# Native Mongo FastAPI App

Requires Node, Docker

## Server

With .env in root directory:

```
docker compose build
docker compose up
```

## Client

```
cd NMFTApp
npm install
npm start
```

## Testing Script

- Start Server

- Then run:

```
python scripts/server_test_script.py
```