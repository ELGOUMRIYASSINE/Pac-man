SRC=pac-man.py
PY=python
UV=uv 

install:
	@$(UV) sync || true

run:
	@$(UV) run $(PY) $(SRC) $(ARG)

debug:
	@$(UV) run $(PY) -m pdb $(SRC) $(ARGS) || true
#build: -> to be added

clean:
	@cleanpy . || true

lint:
	@flake8 . || true
	@mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs || true

