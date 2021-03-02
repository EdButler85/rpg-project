#!/bin/bash
if [ ! -d .env ]; then
	python3 -m venv .venv;
fi

if [ -z "$VIRTUAL_ENV" ]; then
	source .venv/bin/activate;
fi

pip install -r requirements.txt;