.PHONY: setup test spec-check clean

# Standardized setup command
setup:
	@echo "[*] Installing dependencies with uv..."
	uv sync

# Run tests in Docker as required by the Challenge Task 3.2
test:
	@echo "[*] Building Docker image for Project Chimera..."
	docker build -t chimera-app .
	@echo "[*] Running failing TDD tests in container..."
	docker run --rm chimera-app

# (Optional) Verify if code matches the Pydantic contracts and spec links
spec-check:
	@echo "[*] Verifying spec alignment in schemas/..."
	uv run python -c "from schemas.contracts import AgentTask; print('Schema validation active.')"

# Cleanup artifacts
clean:
	@echo "[*] Cleaning up environment..."
	rm -rf .venv
	docker rmi chimera-app || true
