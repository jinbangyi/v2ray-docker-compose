# 
# /bin/bash scripts/upstream.sh

cd /tmp
git clone https://github.com/jinbangyi/v2ray-docker-compose.git
cd v2ray-docker-compose

rm -rf running
mkdir running
cp -r v2ray-upstream-server/* running/
# cp -r utils running/

cd running/

# /bin/bash ./utils/bbr.sh
sed -i 's/<UPSTREAM-UUID>/'`cat /proc/sys/kernel/random/uuid`'/g' v2ray/config/config.json

docker-compose up -d
