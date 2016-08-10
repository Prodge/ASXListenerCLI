VIRTUAL_ENV = venv
PYTHON = $(VIRTUAL_ENV)/bin/python3
PIP = $(VIRTUAL_ENV)/bin/pip3

NAME = asxlistener

INSTALL_BASE = /usr/local/bin
INSTALL_DIR = $(INSTALL_BASE)/$(NAME)-bin
INSTALL_EXE = $(INSTALL_BASE)/$(NAME)

venv:
	virtualenv -p /usr/bin/python3 venv;
	$(PIP) install -r ./requirements.txt

clear_venv:
	rm -rf ./venv

uninstall:
	rm -rf $(INSTALL_DIR)
	rm -f $(INSTALL_EXE)

install: venv uninstall
	# Create folder for dependencies
	mkdir $(INSTALL_DIR)
	# Move Virtual environment and script
	cp -r ./$(VIRTUAL_ENV) $(INSTALL_DIR)/$(VIRTUAL_ENV)
	cp ./$(NAME).py $(INSTALL_DIR)/$(NAME).py
	# Create executable script for running python script with the virtual environment
	echo "#!/bin/bash" >> $(INSTALL_EXE)
	echo "$(INSTALL_DIR)/$(PYTHON) $(INSTALL_DIR)/$(NAME).py" >> $(INSTALL_EXE)
	chmod +x $(INSTALL_EXE)
