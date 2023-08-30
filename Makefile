.PHONY: install run

venv:
	`which python3.11` -m venv venv
	venv/bin/pip install pip==23.2.1 pip-tools wheel --no-cache-dir

requirements.txt: venv requirements.in
	venv/bin/pip-compile -o requirements.txt --no-header --no-emit-index-url --no-emit-trusted-host requirements.in

setup: requirements.txt
	venv/bin/pip-sync requirements.txt
	mkdir ${PWD}/dagster_home	

run: dagster_home
	export DAGSTER_HOME=${PWD}/dagster_home && \
	venv/bin/dagit -p 3000
