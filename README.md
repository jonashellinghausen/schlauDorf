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

The project is licensed under the MIT License. See [LICENSE](LICENSE) for
details.
