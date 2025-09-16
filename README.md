# schlauDorf

This repository contains the initial scaffold for the **schlauDorf** village application built with Flask.

## Development setup

Run the provided installation script to fetch required system and Python
dependencies. It creates a virtual environment and installs everything from
`requirements.txt`.

```bash
./install.sh
source venv/bin/activate
flask --app run.py db upgrade
FLASK_DEBUG=1 flask --app run.py run
```

## Production deployment

Use the included `deploy.sh` helper to apply database migrations and start the
Socket.IO-enabled Gunicorn server without enabling the Flask debugger:

```bash
./deploy.sh
```

The script honours environment variables defined in a local `.env` file and
runs `flask db upgrade` before delegating to Gunicorn.

## Configuration

The application picks its configuration class based on the `FLASK_CONFIG`
environment variable. When the variable is not set the default development
configuration is used. Set `FLASK_CONFIG=production` (or provide the full
import path to a configuration class) to activate the production settings.

The production configuration requires two environment variables to be present
before the app starts:

* `SECRET_KEY` – the Flask secret key used to sign session cookies.
* `DATABASE_URL` – SQLAlchemy connection string for the production database.

Example invocation:

```bash
export SECRET_KEY='change-me'
export DATABASE_URL='postgresql://user:password@host:5432/dbname'
export FLASK_CONFIG=production
flask --app run.py run
```

The project is licensed under the MIT License. See [LICENSE](LICENSE) for
details.
