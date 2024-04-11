set -e

cd /tmp
rm -rf v2ray-docker-compose

# git clone https://github.com/jinbangyi/v2ray-docker-compose.git
git clone https://gitee.com/jinbangy/v2ray-docker-compose.git
cd v2ray-docker-compose

mkdir running
cp -r v2ray-relay-server/* running/
# cp -r utils running/
cd running/
mkdir logs
# /bin/bash ./utils/bbr.sh
IP=`curl ifconfig.me`
# sed -i 's/<BRIDGE-UUID>/'`cat /proc/sys/kernel/random/uuid`'/g' v2ray/config/config.json
# sed -i 's/<RELAY-IP>/'$IP'/g' caddy/config/Caddyfile
# # upstream ip
# sed -i 's/<UPSTREAM-IP>/'$1'/g' v2ray/config/config.json
# upstream uuid
UUID=`cat /proc/sys/kernel/random/uuid`
echo UUID: $UUID

sed -i 's/<RELAY-IP>/'$IP'/g' caddy/config/Caddyfile
sed -i 's/<RELAY-UUID>/'$UUID'/g' v2ray/config/config.json

/bin/bash ../scripts/tls.sh $IP '172.19.10.2'
mv cert.pem key.pem caddy/config/

cd ../subscriber
cp -r ../running/v2ray .
docker build . -t benny-subscriber

cd ../running/
docker-compose down
docker-compose up -d
