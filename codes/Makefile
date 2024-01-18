SHELL := /bin/bash

COLOR := \033[0;35m
GREEN := \033[0;32m
RED := \033[0;31m
RESET := \033[0m

.PHONY: all run setup clean

all: setup run

run: setup main.py $(wildcard *.py)
	@echo "Running main.py"
	@python main.py

%: %.py
	@echo "Running $<"
	@python $<

setup_flag := .setup_done

setup:$(setup_flag)
$(setup_flag):
	@echo -e "${COLOR}Setting up virtual environment ${RESET}"
	@python3 -m venv venv || echo -e "${RED} Oops! Please install virtual environment :) ${RESET}"
	@echo -e "${COLOR}Activating virtual environment ${RESET}"
	@source venv/bin/activate && \
	pip install -r requirements.txt || echo -e "${RED} Oops! Please install ${GREEN}pip${RED} python package manager :) ${RESET}"
	@echo -e "${GREEN}Setup complete :D${RESET}"
	@touch $(setup_flag)

clean:
	@rm -rf venv __pycache__ $(setup_flag) 
	@echo -e "${GREEN}The environment Cleaned up. Be a nice person :) ${RESET}"

.DEFAULT_GOAL := all
