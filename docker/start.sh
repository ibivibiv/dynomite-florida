#!/bin/bash
#trickery here to use the ordinal id to give that rackname for the config for dynomite
export ORDINAL_ID=${HOSTNAME##*-} 
export RACK_ID='us-east-'$ORDINAL_ID'b'
envsubst '$RACK_ID' <conf/redis_single.yml | tee conf/redis_single.yml
envsubst '${DYNO_TOKEN}' <conf/redis_single.yml | tee conf/redis_single.yml
#Start redis server on 22122
redis-server --port 22122 &
#Start the local proxy for florida... comment this out if you did something else here or maybe you are starting python version?
nodejs proxy.js &
src/dynomite --conf-file=conf/redis_single.yml -v11
