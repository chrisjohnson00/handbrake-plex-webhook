# handbrake-plex-webhook
A webhook receiver from Plex that will trigger a watched show to be downgraded in resolution

## Local setup

    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt

## Run Locally

    export FLASK_ENV=development
    flask run