# 
# /bin/bash scripts/upstream.sh
set -e

if [ -z $2 ]; then echo 'must input uuid and ip: grep id ~/temp/v2ray-docker-compose/v2ray/config/v2ray.config'; exit 1; fi;

rm -rf ~/temp
mkdir ~/temp
cd ~/temp

rm -rf v2ray-docker-compose
git clone https://github.com/jinbangyi/v2ray-docker-compose.git
cd v2ray-docker-compose

docker rm -f running-v2ray-1
mkdir running
cp -r v2ray-upstream-server/* running/
# cp -r utils running/

cd running/
mkdir logs
# IP=`curl ifconfig.me`

# /bin/bash ./utils/bbr.sh
sed -i 's/<RELAY-UUID>/'$1'/g' v2ray/config/config.json
sed -i 's/<RELAY-IP>/'$2'/g' v2ray/config/config.json

docker-compose up -d
