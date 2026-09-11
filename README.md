# hello-temporal-demo

A minimal Temporal "hello world" in Python. Runs against either a local dev server or
Temporal Cloud with no code changes — the target is set entirely in `.env`, resolved by the
`temporalio.envconfig` helpers.

## Setup

```bash
uv sync
cp .env.example .env
```

`.env.example` ships with the local dev server active and commented blocks for Temporal
Cloud (API key or mTLS). Uncomment the one you want and comment out the rest. `.env` is
gitignored; `.env.example` is not.

Get an API key from the Temporal Cloud UI under **Settings → API Keys**. Note that API key
auth uses the *regional* endpoint (`us-east-2.aws.api.temporal.io:7233`), not the
per-namespace `.tmprl.cloud` one.

## Run

```bash
make            # list targets
make local      # start a local Temporal dev server (only for local runs)
make worker     # run the worker — leave running
make run        # start one workflow
```

Local:

```
✅ Client connected to localhost:7233 in namespace 'default'
Result: Hello, Temporal!
```

Cloud:

```
✅ Client connected to us-east-2.aws.api.temporal.io:7233 in namespace 'jgs-demo.sdvdw'
Result: Hello, Temporal!
```

If `make run` hangs instead of printing, the worker isn't running — the workflow sits in
`Running` with nothing polling for it.

Web UI: http://localhost:8233 locally, or the Temporal Cloud UI.

## How the connection works

Both `worker.py` and `starter.py` connect with the same canonical two lines:

```python
connect_config = ClientConfig.load_client_connect_config()
client = await Client.connect(**connect_config)
```

`load_client_connect_config()` reads `TEMPORAL_ADDRESS`, `TEMPORAL_NAMESPACE`,
`TEMPORAL_API_KEY` and friends from the environment. `load_dotenv()` runs first and loads
`.env` into that environment — it does **not** override variables already exported in your
shell, so a real environment variable always beats the file.

TLS is inferred rather than configured: supplying an API key enables it automatically,
which is why there is no `tls=True` anywhere in the code. The same two lines produce a
plaintext localhost connection or a TLS Cloud connection based only on `.env`.

Anything not set falls back to the `default` profile in
`~/.config/temporalio/temporal.toml` (`~/Library/Application Support/temporalio/` on macOS)
if that file exists. Pass `disable_file=True` if you'd rather rule that out.

See [Environment configuration](https://docs.temporal.io/develop/environment-configuration).

## Layout

```
activities/greet.py    # the activity
workflows/greeting.py  # the workflow
worker.py              # runs the worker
starter.py             # starts one workflow
.env.example           # template — copy to .env
Makefile               # local / worker / run
```

Workflows and activities live in separate files on purpose: the Python SDK re-imports
workflow modules in a sandbox on every execution, so keeping them small keeps the worker
fast.
