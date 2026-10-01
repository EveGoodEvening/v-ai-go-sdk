# Release readiness and policy

## Current release policy

The owner selected the simple publication path on 2026-09-30: commit and push the release changes, push a version tag, and let GitHub Actions publish after automated checks. Project-authored work uses root [`LICENSE`](../LICENSE) (MIT); retain the Apache-2.0 portions and notices described in [`THIRD_PARTY_NOTICES.md`](../THIRD_PARTY_NOTICES.md). The [`release` environment](https://github.com/EveGoodEvening/v-ai-go-sdk/deployments/activity_log?environments_filter=release) exists; master-branch protection, required reviewers, and `RELEASE_APPROVED_SHA` are not required.

The current version is `v0.2.0`, the experimental `v-ai-go-sdk` module-path and attribution correction. The general public-generation and provider-evaluation live suites remain **NOT RUN / PENDING LIVE RUN**, and staged modalities have no hosted success evidence. Publication retains those limitations rather than marking the evidence complete. See the [live evidence record](evaluation-live-evidence.md) for the narrower completed search probes and unresolved live behavior. Publishing does not authorize additional paid calls.

This current policy supersedes the historical manual release blockers in the implementation plan. Automated CI, versioned migration notes, immutable tags, module verification, and honest evidence remain required.

[`v0.1.0`](https://github.com/EveGoodEvening/v-ai-go-sdk/releases/tag/v0.1.0) was published on 2026-09-30 from commit `2a81fb87d68bae4ea7cfda90489df9b1559b986c`. Both the [branch CI](https://github.com/EveGoodEvening/v-ai-go-sdk/actions/runs/36692946639) and [tag release workflow](https://github.com/EveGoodEvening/v-ai-go-sdk/actions/runs/36693828990) passed. Independent direct-Git and public-proxy downloads compiled and ran successfully with matching module checksums. The release includes its versioned notes, verification manifest, checksums, and attestation bundle; these are publication/consumer evidence, not Gateway live-contract evidence.

[`v0.2.0`](https://github.com/EveGoodEvening/v-ai-go-sdk/releases/tag/v0.2.0) is published as Latest from commit `1838f6e55e57160b9dfb08aeed57390e6b2c32ca`. Its [branch CI](https://github.com/EveGoodEvening/v-ai-go-sdk/actions/runs/36705563323) and [tag release workflow](https://github.com/EveGoodEvening/v-ai-go-sdk/actions/runs/36706239485) succeeded. Independent new-path direct-Git and public-proxy consumers built, ran and verified matching checksums with `sum.golang.org`; the public module ZIP retains the MIT/Apache licenses, attribution inventory and all three modification notices. All four release asset digests and the attestation payload's manifest-digest binding were checked; this was not an independent cryptographic signature-verification run. The original v0.1.0 tag remains unchanged.

## Publish a version

1. Put the version's changes in an exact changelog heading such as `## v0.2.0`. Include a nonempty `### Migration` section naming every required caller action, or state that none is required. Keep `## Unreleased` for subsequent work. Release notes never fall back to Unreleased.
2. Commit and push the release changes to `master`. Wait for ordinary CI to pass before pushing an immutable tag:

   ```sh
   git tag -a v0.2.0 -m "Release v0.2.0"
   git push origin v0.2.0
   ```

3. The [Release workflow](../.github/workflows/release.yml) verifies and publishes automatically. No reviewer action or manual SHA variable is needed. It uses the automatic `GITHUB_TOKEN`, not a personal access token or Gateway API key.

Use a fresh version for each release. Tags such as `v0.2.0-rc.1` produce GitHub prereleases and are never marked Latest. Canonical v0 semantic versions are supported; build metadata is not. The workflow does not create missing tags or overwrite existing releases.

## Automatic checks and artifacts

Branch/PR CI and tag verification share the pinned [CI workflow](../.github/workflows/ci.yml):

| Go version | Required checks |
| --- | --- |
| 1.26.8 and 1.27.1 | Ordinary hermetic suite and example compilation |
| 1.27.1 | Race detector, `go vet`, [clean local consumer](../scripts/verify-local-consumer.sh) |

Ordinary checks unset Gateway credentials and live acknowledgements, and the test transport guard rejects non-loopback traffic. Changing a toolchain pin requires a reviewed compatibility/evidence update; do not use floating Go versions.

After CI, publishing:

- extracts only the tagged version's changelog section and checks its Migration notes;
- downloads the exact Go module through direct Git and `https://proxy.golang.org` with separate clean module caches and `sum.golang.org` verification;
- checks the direct tag's commit against the workflow commit and compares both module checksums **before executing the downloaded code**;
- builds and runs a credential-free consumer without a local `replace`, then runs `go mod verify`;
- signs the structural verification manifest and creates the GitHub Release.

Only the publishing job receives `contents: write`, `attestations: write`, and `id-token: write`. Ordinary CI remains read-only. The repository must allow the official GitHub actions and these job permissions. Attestation supports public repositories on supported GitHub plans, or private repositories on Enterprise Cloud.

Release assets are `release-notes.md`, `release-evidence.json`, `SHA256SUMS`, and `provenance.sigstore.json`. The attestation covers the verification manifest, not a compiled SDK binary or paid Gateway success. After downloading the assets:

```sh
sha256sum -c SHA256SUMS
gh attestation verify release-evidence.json --repo EveGoodEvening/v-ai-go-sdk
```

Retained evidence must remain structural and pass the applicable [sanitization review](evaluation-live-evidence.md#sanitization-review). Do not retain credentials, prompts, generated content, or raw Gateway payloads in release artifacts.

## Live workflow boundary

[`live-contract.yml`](../.github/workflows/live-contract.yml) remains separate from ordinary CI and tag releases. Its public-generation and provider-evaluation jobs require their own credentials, cost acknowledgements, and authorization. The completed configurable `x_search` probes must not be rerun merely to publish a release. No tag workflow invokes paid Gateway APIs.

A local fixture, green CI run, module download, attestation, or published version is not evidence of live API compatibility. Preserve the exact supported request-only search boundaries and experimental modality limitations in the guides and changelog.

## v0 compatibility and migration

Releases remain `v0.x`; no v1 stability is promised while evaluation and staged provider protocols are experimental. Every exported breaking change, including during v0, needs a version increment, changelog entry, updated examples/docs, and release-note Migration instructions. Nonbreaking releases state that no caller action is required.

Evaluation callers retain `Evaluate` and `WithBaseURL`; generation uses explicit Responses/Chat methods plus `WithPublicBaseURL`. There are no compatibility aliases or endpoint auto-detection. For v0.2.0, migrate every former-module-path import and `go.mod` entry to `github.com/EveGoodEvening/v-ai-go-sdk`; retain package alias `gateway`. See the [v0.2.0 migration](../CHANGELOG.md#migration).

## Immutable tags and defective releases

**Pushing a Git tag exposes the Go module version before CI or GitHub Release creation finishes.** Wait for branch CI before tagging; the release job can stop GitHub Release creation but cannot hide an already pushed Git tag.

Never move, delete as a rollback, or reuse a published tag, including a failed prerelease candidate. A transient infrastructure/proxy failure can be retried with **Re-run failed jobs** on the same unchanged tag. Existing releases are not overwritten on rerun.

Correct a defective version with a new patch release. Add an appropriate `retract` directive to `go.mod` naming the actual bad version/range and rationale, mark the hosted release as affected, publish corrected notes, and direct consumers to the new version. Issue a security advisory for security-impacting defects. Keep the old tag intact and never add speculative retractions.

### Newly pushed tag reports `unknown revision`

Check version availability through Git refs before tagging, not by requesting a not-yet-pushed version from `proxy.golang.org` or `sum.golang.org`. The [Go module services FAQ](https://proxy.golang.org/) warns that a request made before the tag exists can cache its absence for up to 30 minutes.

`GOPROXY=direct` still uses `sum.golang.org` for checksum verification. A direct download can resolve the correct Git tag and then fail at the checksum lookup with HTTP 404 `unknown revision`. The release script reports Go's JSON `Error` with the download source and leaves stderr visible so this is distinguishable from Git access failures and checksum mismatches.

For a confirmed negative-cache failure, keep the tag unchanged, wait for the public services to resolve that exact version, then use **Re-run failed jobs** on the existing Release run. Do not disable `GOSUMDB`, skip the public-proxy consumer, or move/reuse the tag. A checksum mismatch is not a propagation failure and must be investigated rather than bypassed. Local consumer verification does not establish hosted publication success.

