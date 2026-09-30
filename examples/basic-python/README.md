# Desktop Sandbox Python Example

This is a basic example of how to use the Desktop Sandbox Python SDK with streaming and moving mouse around.

## How to run

### 1. Create `.env` file

```bash
cp .env.example .env
```

### 2. Set `E2B_API_KEY` in `.env` file

Get your API key at [e2b.dev/dashboard](https://e2b.dev/dashboard).

```bash
E2B_API_KEY="your_api_key"
```

### 3. Install dependencies

```bash
uv sync
```

### 4. Run

```bash
uv run python main.py
```

