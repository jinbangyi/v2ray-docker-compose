import base64
import json
import urllib.parse

from pydantic import BaseModel
import requests
import uvicorn
import aiohttp
from fastapi import FastAPI
from starlette.responses import HTMLResponse


class Link(BaseModel):
    id: str
    port: int
    aid: int = 0
    type: str = "vmess"


def get_vmess_subscribe_link(link: Link) -> str:
    resp = requests.get("http://ifconfig.me")
    ip = resp.text
    vmess = {
        "v": 2,
        "ps": f"nftgo-tcp-{ip}",
        "add": ip,
        "type": "none",
        "path": "",
        "net": "tcp",
    }
    vmess["port"] = link.port
    vmess["id"] = link.id
    vmess["aid"] = link.aid

    return (
        f"vmess://{base64.b64encode(json.dumps(vmess).encode('ascii')).decode('ascii')}"
    )


app = FastAPI(
    title="Management API For Automation",
    servers=[
        {"url": "https://example.com/", "description": "Production environment"},
    ],
    version="v0.0.1",
    description="for automation",
)
DEFAULT_APIKEY = "benny"
DEFAULT_SUBSCRIBER_PORT = 29002
# 第三方转换器的端口
DEFAULT_SUBCONVERTER_PORT = 25500
app.apikeys = set([DEFAULT_APIKEY])
app.links = set([])


@app.post("/links")
async def create_link(link: Link):
    vmess_link = get_vmess_subscribe_link(link)
    app.links.add(vmess_link)
    return "success"


@app.get("/subscribe")
async def subscribe(apikey: str):
    if apikey not in app.apikeys:
        return HTMLResponse(content="0", status_code=400)

    res = "\n".join(app.links)
    html = base64.b64encode(res.encode(encoding="utf8"))
    return HTMLResponse(content=html, status_code=200)


@app.get("/subscribe/clash")
async def subscribe_clash(apikey: str):
    if apikey not in app.apikeys:
        return HTMLResponse(content="0", status_code=400)

    link = f"http://subscriber:{DEFAULT_SUBSCRIBER_PORT}/subscribe?apikey={urllib.parse.quote(apikey)}"
    async with aiohttp.ClientSession() as session:
        # 请求第三方转换器
        url = f"http://subconverter:{DEFAULT_SUBCONVERTER_PORT}/sub"
        params = {"target": "clash", "url": link}
        async with session.get(url, params=params) as resp:
            text = await resp.text()
    return HTMLResponse(content=text, status_code=200)


@app.get("/apikey/add/{apikey}")
async def add_apikey(apikey: str):
    app.apikeys.add(apikey)
    return "1"


def start():
    uvicorn.run(
        "subscribe:app",
        host="0.0.0.0",
        port=DEFAULT_SUBSCRIBER_PORT,
        log_level="info",
    )


if __name__ == "__main__":
    start()
