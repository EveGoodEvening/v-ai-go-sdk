# v-ai-go-sdk

Experimental, unofficial Go client for Vercel AI Gateway. Not affiliated with or endorsed by Vercel. Requires **Go 1.26+**; the package name is `gateway`.

| API | Methods |
| --- | --- |
| Responses | `CreateResponse`, `StreamResponse` |
| Chat Completions | `CreateChatCompletion`, `StreamChatCompletion` |
| Evaluation | `Evaluate` |
| Images (staged) | `GenerateImage` |
| Speech (staged) | `GenerateSpeech` |
| Buffered transcription (staged) | `Transcribe` |
| Embeddings (staged) | `Embed` |
| Reranking (staged) | `Rerank` |

**Experimental v0.** Full live-contract suites are pending; staged APIs have no hosted success evidence. See [release policy](docs/releasing.md).

## Quick start

```sh
go get github.com/EveGoodEvening/v-ai-go-sdk
```

Set `AI_GATEWAY_API_KEY` (or `VERCEL_OIDC_TOKEN`), then run the example. It makes a real request and may incur charges.

```go
package main

import (
    "context"
    "fmt"
    "log"
    "time"

    gateway "github.com/EveGoodEvening/v-ai-go-sdk"
)

func main() {
    client, err := gateway.NewClient()
    if err != nil {
        log.Fatal(err)
    }

    ctx, cancel := context.WithTimeout(context.Background(), 30*time.Second)
    defer cancel()

    result, err := client.CreateResponse(ctx, gateway.ResponsesRequest{
        Model: "openai/gpt-5-nano",
        Input: gateway.ResponseTextInput("Explain Go contexts briefly."),
    })
    if err != nil {
        log.Fatal(err)
    }
    fmt.Printf("response completed: raw_json_bytes=%d\n", len(result.RawJSON()))
}
```

`RawJSON()` is not sanitized; this example prints only its size.

## Guides and examples

- [Generation](docs/generation.md): Responses, Chat, streaming, and opt-in search.
- [Evaluation](docs/evaluation.md): typed questions and answers.
- [Client configuration](docs/client.md): authentication, endpoints, retries, errors, privacy, and staged API contracts.
- Runnable examples: [generation](examples/generate/main.go) and [evaluation](examples/evaluate/main.go).
- [Contributing](CONTRIBUTING.md) · [Changelog and migration](CHANGELOG.md) · [Release policy](docs/releasing.md)
- [MIT license](LICENSE) for project-authored work; [third-party notices and adaptation scope](THIRD_PARTY_NOTICES.md) for Apache-2.0 upstream portions.

## Scope

Responses and Chat use public `/v1`; all other methods use provider `/v4/ai`. Search is opt-in and request-only; the SDK never executes tools. This is not a full JavaScript AI SDK port or a general OpenAI client. See [unsupported features](CHANGELOG.md#explicit-non-goals) for the full boundary.

