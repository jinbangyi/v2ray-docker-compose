# 
# /bin/bash scripts/upstream.sh

cd /tmp
rm -rf v2ray-docker-compose
git clone https://github.com/jinbangyi/v2ray-docker-compose.git
cd v2ray-docker-compose

docker rm -f running-v2ray-1
mkdir running
cp -r v2ray-upstream-server/* running/
# cp -r utils running/

cd running/

# /bin/bash ./utils/bbr.sh
sed -i 's/<UPSTREAM-UUID>/'`cat /proc/sys/kernel/random/uuid`'/g' v2ray/config/config.json

docker-compose up -d
