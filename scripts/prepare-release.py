#!/usr/bin/env python3
"""Prepare versioned notes and verify published Go module consumers; no Gateway calls."""

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile


MODULE = "github.com/EveGoodEvening/v-ai-go-sdk"


def validate_tag(tag):
    if not re.fullmatch(r"v0\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)(-[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?", tag):
        raise ValueError("tag must be a canonical v0 semantic version, e.g. v0.1.0 or v0.1.0-rc.1")
    if "-" in tag:
        for identifier in tag.split("-", 1)[1].split("."):
            if identifier.isdigit() and len(identifier) > 1 and identifier.startswith("0"):
                raise ValueError("numeric prerelease identifiers must not have leading zeroes")


def release_notes(tag, changelog):
    sections = re.split(r"^## ", changelog, flags=re.MULTILINE)
    matches = []
    for section in sections[1:]:
        heading, _, body = section.partition("\n")
        if heading.strip() == tag:
            matches.append(body.strip())
    if len(matches) != 1:
        raise ValueError(f"CHANGELOG.md must contain exactly one '## {tag}' section; Unreleased is not a release")
    notes = matches[0]
    migration = re.search(r"^### Migration\s*\n(.*?)(?=^#{1,3} |\Z)", notes, flags=re.MULTILINE | re.DOTALL)
    if migration is None or not migration.group(1).strip():
        raise ValueError("release notes require a nonempty '### Migration' section")
    return notes + "\n"


def consumer(tag, proxy, expected_commit=None, expected_checksums=None):
    """Download and compile the real module in an isolated cache, without a replace."""
    with tempfile.TemporaryDirectory(prefix="gateway-release-consumer-") as temporary:
        root = Path(temporary)
        environment = {
            key: value for key, value in os.environ.items()
            if not key.startswith("AI_GATEWAY_") and key not in ("VERCEL_OIDC_TOKEN", "GH_TOKEN", "GITHUB_TOKEN")
        }
        environment.update({
            "GOENV": "off", "GOFLAGS": "", "GOWORK": "off", "GOPROXY": proxy,
            "GOPRIVATE": "", "GONOPROXY": "", "GONOSUMDB": "", "GOINSECURE": "",
            "GOMODCACHE": str(root / "modules"),
        })
        (root / "go.mod").write_text(
            f"module example.com/gateway-release-consumer\n\ngo 1.26\n\nrequire {MODULE} {tag}\n",
            encoding="utf-8",
        )
        (root / "main.go").write_text(
            'package main\n\nimport gateway "' + MODULE + '"\n\n'
            'func main() {\n'
            '\t_, err := gateway.NewClient(gateway.WithAPIKey("local-release-check"))\n'
            '\tif err != nil { panic(err) }\n'
            '}\n',
            encoding="utf-8",
        )
        downloaded = subprocess.run(
            ["go", "mod", "download", "-json", f"{MODULE}@{tag}"], cwd=root,
            env=environment, stdout=subprocess.PIPE, text=True,
        )
        module = json.loads(downloaded.stdout) if downloaded.stdout else {}
        if module.get("Error"):
            raise ValueError(f"module download via {proxy} failed: {module['Error']}")
        downloaded.check_returncode()
        if module.get("Path") != MODULE or module.get("Version") != tag:
            raise ValueError("downloaded module identity does not match the requested release")
        if not module.get("Sum") or not module.get("GoModSum"):
            raise ValueError("downloaded module is missing Go checksums")
        if expected_commit is not None and module.get("Origin", {}).get("Hash") != expected_commit:
            raise ValueError("direct-VCS tag does not resolve to the workflow commit")
        if expected_checksums is not None and (module["Sum"], module["GoModSum"]) != expected_checksums:
            raise ValueError("direct-VCS and public-proxy module checksums differ")
        subprocess.run(["go", "build", "-mod=readonly", "-o", "consumer", "."], cwd=root, env=environment, check=True)
        subprocess.run([str(root / "consumer")], cwd=root, env=environment, check=True)
        subprocess.run(["go", "mod", "verify"], cwd=root, env=environment, check=True)
        return {
            "source": proxy,
            "sum": module["Sum"],
            "go_mod_sum": module["GoModSum"],
            "commit": module.get("Origin", {}).get("Hash"),
        }


def verify(tag, output):
    commit = os.environ["GITHUB_SHA"]
    direct = consumer(tag, "direct", expected_commit=commit)
    proxy = consumer(tag, "https://proxy.golang.org", expected_checksums=(direct["sum"], direct["go_mod_sum"]))
    evidence = {
        "module": MODULE,
        "version": tag,
        "commit": commit,
        "toolchain": subprocess.check_output(["go", "version"], text=True).strip(),
        "workflow_run": f"{os.environ['GITHUB_SERVER_URL']}/{os.environ['GITHUB_REPOSITORY']}/actions/runs/{os.environ['GITHUB_RUN_ID']}",
        "consumers": [direct, proxy],
    }
    (output / "release-evidence.json").write_text(json.dumps(evidence, indent=2) + "\n", encoding="utf-8")
    checksums = []
    for name in ("release-notes.md", "release-evidence.json"):
        digest = hashlib.sha256((output / name).read_bytes()).hexdigest()
        checksums.append(f"{digest}  {name}\n")
    (output / "SHA256SUMS").write_text("".join(checksums), encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("notes", "verify"))
    parser.add_argument("tag")
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    try:
        validate_tag(args.tag)
        args.output.mkdir(parents=True, exist_ok=True)
        if args.command == "notes":
            notes = release_notes(args.tag, Path("CHANGELOG.md").read_text(encoding="utf-8"))
            (args.output / "release-notes.md").write_text(notes, encoding="utf-8")
            if "GITHUB_OUTPUT" in os.environ:
                with open(os.environ["GITHUB_OUTPUT"], "a", encoding="utf-8") as output:
                    output.write(f"prerelease={str('-' in args.tag).lower()}\n")
        else:
            verify(args.tag, args.output)
    except (ValueError, KeyError, OSError, subprocess.CalledProcessError) as error:
        parser.exit(1, f"release preparation failed: {error}\n")


if __name__ == "__main__":
    main()
