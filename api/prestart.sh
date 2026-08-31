#!/bin/bash

echo "Running pre start"

PORT="${PORT:-80}"

# Reload watches the bind mounted source in dev, and must stay off everywhere
# else: it restarts the process on any source change, which kills whatever the
# background worker is part way through and empties the job history with it.
if [ "$RELOAD" = "true" ]; then
    exec uvicorn API.main:app --host 0.0.0.0 --port "$PORT" --reload
fi

exec uvicorn API.main:app --host 0.0.0.0 --port "$PORT"
