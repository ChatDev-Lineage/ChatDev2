# ==============================================================================
# Development Commands
# ==============================================================================

.PHONY: dev
dev: ## Run both backend and frontend development servers
	@$(MAKE) -j2 server client


.PHONY: server
server: ## Start the backend server in the background
	@echo "Starting server in background..."
	@uv run python server_main.py --port 6400 &

.PHONY: client
client: ## Start the frontend development server
	@cd frontend && npx cross-env VITE_API_BASE_URL=http://localhost:6400 npm run dev

.PHONY: stop
stop: ## Stop backend and frontend servers cross-platform
	@echo "Stopping backend server (port 6400)..."
	@npx kill-port 6400
	@echo "Stopping frontend server (port 5173)..."
	@npx kill-port 5173

# ==============================================================================
# Tools & Maintenance
# ==============================================================================

.PHONY: sync
sync: ## Sync Vue graphs to the server database
	@uv run python tools/sync_vuegraphs.py

.PHONY: validate-yamls
validate-yamls: ## Validate all YAML configuration files
	@uv run python tools/validate_all_yamls.py

.PHONY: doctor-colony
doctor-colony: ## Probe live ChatDev colony service, local app imports, and route drift
	@python tools/chatdev_colony_doctor.py

.PHONY: doctor-gamedev
doctor-gamedev: ## Print colony truth plus GameDev Python lane compatibility as JSON
	@powershell -NoProfile -ExecutionPolicy Bypass -File .\tools\chatdev_gamedev_lane.ps1 doctor -Json

.PHONY: prove-local-app
prove-local-app: ## Run a bounded local DevAll app proof with startup-route checks
	@powershell -NoProfile -ExecutionPolicy Bypass -File .\tools\chatdev_gamedev_lane.ps1 local-proof -Json

.PHONY: start-local-app
start-local-app: ## Start the local DevAll app in the background and wait for /health
	@powershell -NoProfile -ExecutionPolicy Bypass -File .\tools\chatdev_gamedev_lane.ps1 local-start

.PHONY: stop-local-app
stop-local-app: ## Stop the managed local DevAll app instance
	@powershell -NoProfile -ExecutionPolicy Bypass -File .\tools\chatdev_gamedev_lane.ps1 local-stop

.PHONY: status-local-app
status-local-app: ## Report managed local DevAll app status plus /health
	@powershell -NoProfile -ExecutionPolicy Bypass -File .\tools\chatdev_gamedev_lane.ps1 local-status

.PHONY: bootstrap-gamedev-env
bootstrap-gamedev-env: ## Create the repo-local Python 3.13 GameDev env with pygame support
	@powershell -NoProfile -ExecutionPolicy Bypass -File .\tools\bootstrap_gamedev_env.ps1

.PHONY: smoke-gamedev-mechanic
smoke-gamedev-mechanic: ## Run the proven repo-local GameDev mechanic smoke lane
	@powershell -NoProfile -ExecutionPolicy Bypass -File .\tools\run_gamedev_mechanic_smoke.ps1

.PHONY: latest-gamedev-smoke
latest-gamedev-smoke: ## Print the compact latest bounded smoke receipt summary
	@powershell -NoProfile -ExecutionPolicy Bypass -File .\tools\chatdev_gamedev_lane.ps1 latest

.PHONY: latest-gamedev-smoke-full
latest-gamedev-smoke-full: ## Print the full latest bounded smoke receipt payload
	@powershell -NoProfile -ExecutionPolicy Bypass -File .\tools\chatdev_gamedev_lane.ps1 latest-full

.PHONY: status-gamedev
status-gamedev: ## Print the full combined GameDev status report
	@powershell -NoProfile -ExecutionPolicy Bypass -File .\tools\chatdev_gamedev_lane.ps1 status-full

.PHONY: status-gamedev-compact
status-gamedev-compact: ## Print the compact automation_summary contract for the GameDev smoke lane
	@powershell -NoProfile -ExecutionPolicy Bypass -File .\tools\chatdev_gamedev_lane.ps1 status-compact

# ==============================================================================
# Help
# ==============================================================================

.PHONY: help
help: ## Display this help message
	@uv run python -c "import re; \
	p=r'$(firstword $(MAKEFILE_LIST))'.strip(); \
	[print(f'{m[0]:<20} {m[1]}') for m in re.findall(r'^([a-zA-Z_-]+):.*?## (.*)$$', open(p, encoding='utf-8').read(), re.M)]" | sort

# ==============================================================================
# Quality Checks
# ==============================================================================

.PHONY: check-backend
check-backend: ## Run backend quality checks (tests + linting)
	@$(MAKE) backend-tests
	@$(MAKE) backend-lint

.PHONY: backend-tests
backend-tests: ## Run backend tests
	@uv run pytest -v

.PHONY: backend-lint
backend-lint: ## Run backend linting
	@uvx ruff check .
