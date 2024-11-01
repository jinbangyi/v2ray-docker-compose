cd vmess-server
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
# generate config
.venv/bin/python3 vmess-server.py
# run server
docker-compose up -d
