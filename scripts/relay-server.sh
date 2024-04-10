cd /tmp
rm -rf v2ray-docker-compose

git clone https://github.com/jinbangyi/v2ray-docker-compose.git
cd v2ray-docker-compose

cd subscriber
docker build . -t benny-subscriber
cd ..

mkdir running
cp -r v2ray-relay-server/* running/
# cp -r utils running/
cd running/

# /bin/bash ./utils/bbr.sh
IP=`curl ifconfig.me`
sed -i 's/<BRIDGE-UUID>/'`cat /proc/sys/kernel/random/uuid`'/g' v2ray/config/config.json
sed -i 's/<RELAY-IP>/'$IP'/g' caddy/config/Caddyfile
# upstream ip
sed -i 's/<UPSTREAM-IP>/'$1'/g' v2ray/config/config.json
# upstream uuid
sed -i 's/<UPSTREAM-UUID>/'$2'/g' v2ray/config/config.json

docker-compose up -d
