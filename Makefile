.DEFAULT_GOAL := help
UV := uv run

.PHONY: help local worker run

help:  ## Show this help
	@grep -E '^[a-z-]+:.*?## ' $(MAKEFILE_LIST) | \
		awk 'BEGIN{FS=":.*?## "}{printf "  \033[36m%-8s\033[0m %s\n", $$1, $$2}'

local:  ## Start a local Temporal dev server (run in its own pane)
	temporal server start-dev

worker:  ## Run the worker (run in its own pane)
	$(UV) python worker.py

run:  ## Start one workflow against the running worker
	$(UV) python starter.py
