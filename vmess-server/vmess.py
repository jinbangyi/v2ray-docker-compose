import json
from pathlib import Path

from pydantic import BaseModel
import requests
import click


class Link(BaseModel):
    id: str
    port: int
    aid: int = 0
    type: str = "vmess"
    ip: str = ""


def get_vmess_server_config(uuid: str, port: int = 10150) -> dict:
    base_config = {
        "log": {
            "access": "/var/log/v2ray/access.log",
            "error": "/var/log/v2ray/error.log",
            "loglevel": "debug",
        },
        "inbounds": [
            # 接受客户端
            {
                "tag": "external",
                "port": port,
                "protocol": "vmess",
                "settings": {"clients": [{"id": uuid, "alterId": 0}]},
                "streamSettings": {
                    "network": "tcp",
                    "tcpSettings": {"header": {"type": "none"}},
                },
                "sniffing": {"enabled": True, "destOverride": ["http", "tls"]},
            },
        ],
        "routing": {
            "rules": [
                # 不允许客户端访问服务端的局域网地址，以提升安全性
                {"type": "field", "ip": ["geoip:private"], "outboundTag": "block"},
                {"type": "field", "inboundTag": ["external"], "outboundTag": "direct"},
            ]
        },
        "transport": {
            "kcpSettings": {
                "uplinkCapacity": 100,
                "downlinkCapacity": 100,
                "congestion": True,
            }
        },
        "dns": {"servers": ["8.8.8.8", "1.1.1.1", "localhost"]},
        "outbounds": [
            {
                "protocol": "freedom",
                "settings": {"domainStrategy": "UseIP"},
                "tag": "direct",
            },
            {"protocol": "blackhole", "settings": {}, "tag": "blocked"},
        ],
    }

    return base_config


@click.command()
@click.option("--domain", help="remote domain")
@click.option("--remote_port", default=29002, help="remote port")
def start(domain: str, remote_port: int):
    uuid_path = "/proc/sys/kernel/random/uuid"
    config_path = Path.cwd().joinpath("config.json")
    with open(uuid_path) as f:
        uuid = f.read()

    port = 10150
    vmess_server_config = get_vmess_server_config(uuid, port)
    with open(config_path, "w") as f:
        json.dump(vmess_server_config, f)

    remote_domain = domain
    resp = requests.get("http://ifconfig.me")
    ip = resp.text

    resp = requests.post(
        f"http://{remote_domain}:{remote_port}/links",
        data=Link(id=uuid, port=port, ip=ip).json(),
    )
    if resp.status_code != 200:
        raise Exception("Failed to upload link")


if __name__ == "__main__":
    start()
