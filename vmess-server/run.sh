cd vmess-server
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
# generate config
.venv/bin/python3 vmess.py --domain=xx --remote_port=29002
# run server
docker-compose up -d
