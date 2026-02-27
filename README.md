# Message Trust AI Platform

Dockerized FastAPI app for:
1. Uploading labeled TXT data and training a FastText model
2. Testing SMS messages against the trained model

## URL
- /train
- /test

When deployed behind the current reverse proxy:
- https://openclaw.mdriaz.com.bd/message-trust-ai/
- https://openclaw.mdriaz.com.bd/message-trust-ai/test

## Training format
Each line in TXT:

__label__clear AcmeBank: Your OTP is 1234
__label__unclear Your OTP is 1234

## Deploy
```bash
docker compose up -d --build
```
