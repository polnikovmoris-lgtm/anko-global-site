.PHONY: check static php-lint js-check python-check serve

PYTHON ?= python3
PHP ?= php
AUDIT_OUTPUT ?= /tmp/anko-global-static-audit.json

check: static php-lint js-check python-check

static:
	$(PYTHON) tools/run_final_static_audit.py site --output $(AUDIT_OUTPUT)

php-lint:
	@command -v $(PHP) >/dev/null 2>&1 || { \
		echo "PHP не установлен: установите PHP 7.4+ и повторите make php-lint"; \
		exit 1; \
	}
	@find site -type f -name '*.php' -print0 | \
		xargs -0 -n1 $(PHP) -l >/tmp/anko-global-php-lint.txt
	@echo "PHP lint: OK"

js-check:
	@find site/js -type f -name '*.js' -print0 | xargs -0 -n1 node --check
	@echo "JavaScript syntax: OK"

python-check:
	@$(PYTHON) -m compileall -q tools audit
	@echo "Python syntax: OK"

serve:
	@command -v $(PHP) >/dev/null 2>&1 || { \
		echo "PHP не установлен: установите PHP 7.4+"; \
		exit 1; \
	}
	$(PHP) -S 127.0.0.1:8080 -t site

