SRC=pac-man.py
FOLDER=src
PY=python
UV=uv 

install:
	@$(UV) sync --active || true
	

run:
	@$(UV) run $(PY) $(SRC) $(ARG) || true

debug:
	@$(UV) run $(PY) -m pdb $(SRC) $(ARGS) || true
#build: -> to be added

clean:
	@cleanpy . || true
	@rm -rf .dist || true

lint:
	@flake8 $(SRC) $(FOLDER) || true
	@mypy $(SRC) $(FOLDER) --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs || true

