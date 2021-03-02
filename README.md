# RPG Project

## About

Website for RPG Character Management

## Getting Started

These instructions assume you're using either Linux or macOS. The setup scripts will work on both, but on Windows you'll have to do the work of those yourself. Open up those files to see what they're doing, it isn't all that much.

The easy way:

```bash
./setup.sh
./start.sh
```

The manual way:

* Create or activate an existing [virtualenv](https://docs.python.org/3/library/venv.html)
* Install requirements: `pip install -r requirements.txt`
* Create the database if you don't already have one: `sqlite3 game_stats.db < game_stats.sql`
* Start the application: `FLASK_APP=application FLASK_DEBUG=1 FLASK_ENV=development python -m flask run`