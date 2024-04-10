import base64
import os
import subprocess
import json
import requests

import uvicorn
import aiohttp
from fastapi import FastAPI
from starlette.responses import HTMLResponse
# from apscheduler.schedulers.background import BackgroundScheduler
# from apscheduler.triggers.cron import CronTrigger

def get_vmess_links():
    resp = requests.get('http://ifconfig.me')
    ip = resp.text
    # {"v":2,"ps":"233boy-tcp-116.62.45.83","add":"116.62.45.83","port":"10150","id":"86073f49-e92d-4af4-8abf-d20d58f9d41b","aid":"0","net":"tcp","type":"none","path":""}
    vmess = {
        "v": 2,
        "ps": f"nftgo-tcp-{ip}",
        "add": ip,
        "aid": "0",
        "type": "none",
        "path": "",
        "net": "tcp"
    }
    with open(r'v2ray/config/config.json') as f:
        config = json.loads(f.read())
        vmess_config = list(filter(lambda item: item.get('protocol') == 'vmess', config.get('inbounds', [])))
        if len(vmess_config) > 0:
            vmess['port'] = vmess_config[0]['port']
            vmess['id'] = vmess_config[0]['settings']['clients'][0]['id']

    return base64.b64encode(json.dumps(vmess).encode('utf8')).decode()

def get_v2ray_links() -> list:
    link = get_vmess_links()
    return [f'vmess://{link}']


# def replace_https_port():
#     print(1)
#     https_port = subprocess.getoutput("grep https_port /etc/caddy/Caddyfile | awk '{ print $2 }'")
#     replace_port = os.system(f"sed -ie 's/{https_port}/{str(int(https_port) + 1)}/g' /etc/caddy/Caddyfile")
#     print(replace_port)
#     os.system("v2ray restart")


# scheduler = BackgroundScheduler()
# # Add schedules, configure tasks here
# scheduler.start()
# # cron_trigger = CronTrigger(second=10)
# cron_trigger = CronTrigger(second=0, minute=20, hour=10)
# # Add the job with the cron trigger to the scheduler
# scheduler.add_job(replace_https_port, trigger=cron_trigger, id='replace_port')

app = FastAPI(
    title="Management API For Automation",
    servers=[
        {"url": 'https://example.com/', "description": "Production environment"},
    ],
    version='v0.0.1',
    description='for automation',
)


@app.get('/')
@app.get('/subscribe')
async def subscribe():
    links = get_v2ray_links()
    res = '\n'.join(links)
    html = base64.b64encode(res.encode(encoding='utf8'))
    return HTMLResponse(content=html, status_code=200)

@app.get('/subscribe/clash')
async def subscribe_clash():
    link = 'http://subscriber:29002/subscribe'
    async with aiohttp.ClientSession() as session:
        url = f'http://127.0.0.1:25500/sub?target=clash&url={link}'
        async with session.get(url) as resp:
            text = await resp.text()
    return HTMLResponse(content=text, status_code=200)

def start():
    uvicorn.run(
        "subscribe:app",
        host='0.0.0.0',
        port=29002,
        log_level="info",
    )
    # scheduler.shutdown()


if __name__ == '__main__':
    start()
