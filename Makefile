PYTHON = venv/bin/python3
PIP = venv/bin/pip3

venv:
	virtualenv -p /usr/bin/python3 venv;
	$(PIP) install -r ./requirements.txt

clear_venv:
	rm -rf ./venv
