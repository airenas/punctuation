############################################
-include Makefile.options
############################################
install/req:
	# conda create --name punct python=3.10
	pip install -r requirements.txt

test/unit:
	PYTHONPATH=./ pytest -v --log-level=INFO

test/lint:
	# stop the build if there are Python syntax errors or undefined names
	flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics --exclude .venv,build
	#exit-zero treats all errors as warnings. The GitHub editor is 127 chars wide
	flake8 . --count --max-complexity=10 --max-line-length=127 --statistics --exclude .venv,build
############################################
