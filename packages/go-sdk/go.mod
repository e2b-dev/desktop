module github.com/aj-groq/desktop/packages/go-sdk

go 1.22

require github.com/aj-groq/E2B/packages/go-sdk v0.0.0

require (
	connectrpc.com/connect v1.17.0 // indirect
	google.golang.org/protobuf v1.36.6 // indirect
)

// For local development - point to your local E2B SDK
replace github.com/aj-groq/E2B/packages/go-sdk => ../../../E2B/packages/go-sdk
