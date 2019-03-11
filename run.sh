>&2 echo "Migrations"
./venv/bin/python ./src/models.py

>&2 echo "Bot starting"
./venv/bin/python app.py