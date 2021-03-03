#!/bin/bash
if [ -z "$VIRTUAL_ENV" ]; then
	source .venv/bin/activate;
fi

if [ ! -f game_stats.db ]; then
	echo "Creating empty database"
	sqlite3 game_stats.db < game_stats.sql;
fi

FLASK_APP=application FLASK_DEBUG=1 FLASK_ENV=development python -m flask run;