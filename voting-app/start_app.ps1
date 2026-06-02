$env:REDIS = "127.0.0.1"
$env:REDIS_PWD = "grosmotdepasse"
$env:FLASK_APP = "main.py"
cd azure-vote
..\venv\Scripts\flask run --host=0.0.0.0 --port=8080
