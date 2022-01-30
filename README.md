# esp
Equipements Sportifs Publiques

## Scripts

Create virtual env
```sh
python3 -m venv .venv
```

Install dependencies
```
source .venv/bin/activate
pip install -r requirements.txt
```

### Insert to DB

Start the database
```sh
docker-compose up -d
```

Start the script
```sh
python scripts/insert-to-db.py result_01.xlsx
```
