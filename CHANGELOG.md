# Changelog

## Unreleased

### Fixed

- Release verification now reports Go's JSON module-download error with the download source and retains stderr, instead of hiding the cause behind a subprocess exit status. Checksum and commit checks remain mandatory; no SDK API or runtime behavior changes.

## v0.2.1

### Release preparation

- Restore the versioned release notes required by the automatic tag-release workflow.
- This release-preparation change does not modify SDK APIs, endpoints, or runtime behavior. The package name remains `gateway`; Go 1.26 or newer is required.
- Retain the MIT license for project-authored work and the Apache-2.0 license, attribution inventory, and modification notices for the identified upstream adaptations.

### Migration

Update the module dependency:

```sh
go get github.com/EveGoodEvening/v-ai-go-sdk@v0.2.1
```

No source migration is introduced by this release-preparation change. Callers already using `github.com/EveGoodEvening/v-ai-go-sdk` retain their imports and the `gateway` package name. Callers still using the former module path must replace that old module/import path with `github.com/EveGoodEvening/v-ai-go-sdk`.

### Experimental limitations

- The general public-generation and provider-evaluation live-contract suites remain **NOT RUN / PENDING LIVE RUN**. Staged image, speech, buffered transcription, embedding, and reranking APIs have no hosted success evidence.
- Search support remains opt-in and request-only, limited to the documented declarations and exact evidence-cleared forms. Outputs and unproven events remain raw.
- Automated CI, module-consumer verification, and release attestations are not evidence of live Gateway compatibility. Publishing this version does not authorize or perform paid Gateway calls.
- See the [API guides and scope](https://github.com/EveGoodEvening/v-ai-go-sdk/blob/v0.2.1/README.md) and [live evidence record](https://github.com/EveGoodEvening/v-ai-go-sdk/blob/v0.2.1/docs/evaluation-live-evidence.md) for supported boundaries and outstanding evidence.

### Explicit non-goals

- No full JavaScript AI SDK parity, generic OpenAI client, or direct xAI client.
- No public `/v1/evaluate` implementation; `Evaluate` uses the separate provider-protocol Evaluation Model V4 endpoint.
- No automatic tool execution, agent orchestration, or inferred typed search outputs/events.
- No arbitrary search-option combinations, undocumented search semantics, or wider model-compatibility claims beyond the recorded evidence.
- No v1 stability or claim that pending live-contract gates have passed.
