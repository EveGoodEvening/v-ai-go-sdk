# Third-party notices and source provenance

Project-authored work in v-ai-go-sdk, including its original additions and modifications, is licensed under the [MIT license](LICENSE). The upstream-derived portions identified below retain their Apache-2.0 conditions. The root MIT license does not replace those conditions or offer an MIT-only alternative for upstream material.

## Vercel AI SDK

- Upstream project: <https://github.com/vercel/ai>
- Source baseline: [`ai@7.0.107`](https://github.com/vercel/ai/tree/ai%407.0.107), corresponding to `ai@7.0.107`, `@ai-sdk/gateway@4.0.87`, `@ai-sdk/provider@4.0.17`, and `@ai-sdk/provider-utils@5.0.45` in the implementation evidence. These are source/contract references, not Go runtime dependencies.
- Upstream license: [Apache License, Version 2.0](LICENSES/Apache-2.0.txt).
- The following notice is retained from the [pinned upstream LICENSE](https://github.com/vercel/ai/blob/ai%407.0.107/LICENSE):

```text
Copyright 2023 Vercel, Inc.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
```

The pinned upstream repository root has no separate `NOTICE` file. This document is this project's attribution inventory, not a reproduction of an upstream `NOTICE`.

## Source-derived adaptations

The implementation plan explicitly models evaluation validation on the upstream implementation. The following source-driven validation portions are conservatively treated as adaptations for attribution and redistribution, rather than assuming that translation to Go makes them independent. This does not assert exclusive rights over mathematical formulas, JSON vocabulary, or general validation techniques.

All rows refer to [`packages/ai/src/evaluate/validate-evaluation.ts` at `ai@7.0.107`](https://github.com/vercel/ai/blob/ai%407.0.107/packages/ai/src/evaluate/validate-evaluation.ts). Symbols, rather than line numbers, identify the retained scope.

| Local scope | Upstream source | Modifications made for this project |
| --- | --- | --- |
| [`evaluation_validate.go`](evaluation_validate.go): evaluation-input portions of `validateEvaluationRequest`, `validateQuestion`, `validateBooleanQuestion`, `validateOptionalJSON`, `validateChoiceQuestion`, and `validateScoreQuestion` | `validateEvaluationInput` and its input/criteria acceptance rules | Re-expressed as closed Go value/pointer question types; explicit omitted/null criteria; sorted traversal; path/reason errors; additional model ID, question ID, typed-nil and provider-option checks. |
| [`jsonvalue.go`](jsonvalue.go): `validateJSONInput`, `validateJSONValue`, and `(*jsonValidator).value`, with their ancestry-tracking state | `isInput`, `isJSON`, and `isRecord` | Re-expressed through Go reflection, pointer/interface unwrapping, Go numeric kinds, string-keyed maps, typed-nil handling, sorted traversal, path errors and active-ancestor tracking for Go pointers/maps/slices. JavaScript prototype and symbol-property handling is not retained. |
| [`evaluation_response.go`](evaluation_response.go): `responseBaseTolerance`, `validateResponseAnswers`, `validateBooleanResponse`, `validateChoiceResponse`, `choiceKeys`, `validateScoreResponse`, `validateProbabilityKeys`, and `validateProbabilitySum` | `tolerance`, `validateEvaluationAnswers`, `isProbability`, `hasExactKeys`, `validateDistribution`, and nested `roundingError` | Split into validators over already decoded Go answer types, deterministic key/index traversal and path-based errors. Preserves distribution, maximal-choice, weighted-mean and rounding-tolerance rules without renormalization; score comparison uses explicit lower/upper bounds. Strict JSON decoding happens separately before these checks. |

Each affected file carries a prominent source/copyright/license/modification notice. The unrelated response token-tree parser, bounded decoding, duplicate-key handling, raw-body ownership and metadata parsing in `evaluation_response.go`, and Go-value normalization/path formatting in `jsonvalue.go`, are not attributed to the upstream validator by the table above.

## Protocol and behavior references, not additional identified code adaptations

The remaining comparisons establish interface/behavior provenance, not a claim that every compatible Go implementation is an Apache-derived work. No additional specific source-expression adaptation was identified in these groups. Project-specific implementation and tests are not reassigned to Vercel merely because they use matching field names, endpoints, ordinary fixtures, or standard algorithms.

All upstream repository paths below are relative to [`vercel/ai` at `ai@7.0.107`](https://github.com/vercel/ai/tree/ai%407.0.107).

| Local files or groups | Reference and boundary |
| --- | --- |
| `evaluation.go`, `evaluation_wire.go`, and the wire-decoding portions of `evaluation_response.go` | `packages/gateway/src/gateway-evaluation-model.ts` and `packages/provider/src/evaluation-model/v4/`: request/answer discriminators, fields, warnings, metadata and protocol headers. The Go interfaces, DTO encoding and strict token parser are separate implementations. |
| `auth.go`, `headers.go`, `client.go`, `errors.go`, `provider_options.go` | `packages/gateway/src/gateway-provider.ts` and `gateway-evaluation-model.ts`: API-key/OIDC precedence and protocol constants. Go token-source refresh, protected-header ownership, functional options and safe typed errors are project-specific. |
| `embedding.go`, `embedding_validate.go`, `embedding_wire.go` | `packages/gateway/src/gateway-embedding-model.ts` and `packages/provider/src/embedding-model/v4/`: values/vectors/usage and warning/metadata wire shapes. Exact integer parsing, vector/count/resource validation and owned results are project-specific. |
| `rerank.go`, `rerank_validate.go`, `rerank_wire.go` | `packages/gateway/src/gateway-reranking-model.ts` and `packages/provider/src/reranking-model/v4/`: text/object input and index/relevance-score output. The Go document snapshots, reconstruction, uniqueness/range checks and exact rational index parsing are not ports of Gateway's pass-through result mapping. |
| `image.go`, `image_validate.go`, `image_wire.go` | `packages/gateway/src/gateway-image-model.ts` and `packages/provider/src/image-model/v4/`: request fields, URL/file variants, omission behavior and standard base64 representation. Go byte-result decoding, strict base64 checks, aggregate bounds, JSON-size preflight and ownership are project-specific. |
| `speech.go`, `speech_validate.go`, `speech_wire.go` | `packages/gateway/src/gateway-speech-model.ts` and `packages/provider/src/speech-model/v4/`: text/options, opaque audio and metadata. Go validation, resource bounds and strict decoding are project-specific. |
| `transcription.go`, `transcription_validate.go`, `transcription_wire.go` | Buffered portions of `packages/gateway/src/gateway-transcription-model.ts` and `packages/provider/src/transcription-model/v4/`: audio/media type, text/segments and nullable metadata. Go sealed inputs, once-sized serialization, cancellation/resource checks and strict owned decoding are separate; no upstream WebSocket or streaming implementation is included. |
| `chat.go`, `chat_validate.go`, `chat_wire.go`: the four server-search request families | [Gateway web-search documentation](https://vercel.com/docs/ai-gateway/models-and-providers/web-search), corroborated by `packages/gateway/src/tool/{exa-search,parallel-search,perplexity-search,tako-search}.ts`: tool identifiers, configuration vocabulary, unions and member constraints. Go request-only types, nil/presence handling and serialization do not include the JavaScript tool factories, generated output types or upstream descriptive comments. |
| Other `chat*.go` / `responses*.go` public API code | First-party public Chat/Responses contracts recorded in `planning/IMPLEMENTATION_PLAN.md`; [Gateway SDKs and APIs](https://vercel.com/docs/ai-gateway/sdks-and-apis) provides the current entry points, and search references are listed in [docs/x-search.md](docs/x-search.md#sources). `@ai-sdk/xai@5.0.4` declarations were a direct-provider vocabulary comparison, not a copied provider implementation or Gateway compatibility claim. |
| `retry.go`, `transport.go`, `response_error.go`, `sse.go`, `internal/httpx/`, test helpers, consumer/release scripts | Go HTTP/context/JSON facilities, bounded resource policy and standard HTTP/SSE behavior. These are not vendored JavaScript SDK transport, retry or eventsource-parser implementations. |
| Evaluation/auth/header/modality tests and `examples/evaluate/main.go` | Compared against the corresponding pinned Gateway model tests. Local Go-specific malformed-input, boundary, ownership and cancellation cases differ. Common Paris/France example sentences and `base64-audio` are generic fixture overlap, not evidence sufficient to identify an additional protected-expression adaptation. |

This inventory records the source comparison and attribution decisions for the current implementation; it is not a legal clearance statement or a guarantee about all possible similarities. New copied or adapted material must be added with its own source version, applicable notices and modification description.

## Redistribution

For distributions containing the adapted portions, include the full [Apache-2.0 license](LICENSES/Apache-2.0.txt), preserve the applicable upstream attribution and modification notices, and retain the MIT notice for project-authored work. If future upstream material includes a `NOTICE`, preserve its applicable notices as required by Apache-2.0 section 4. This inventory adds no restrictions to either license.

## Names and trademarks

v-ai-go-sdk is an independent, unofficial client. It is not affiliated with, sponsored by, or endorsed by Vercel. References to Vercel AI Gateway and AI SDK identify compatible services and upstream sources, not project ownership or endorsement. Code licenses do not grant service access or trademark rights.

Vercel, the Vercel design, Next.js and related marks, designs and logos are trademarks or registered trademarks of Vercel, Inc. or its affiliates in the US and other countries.
