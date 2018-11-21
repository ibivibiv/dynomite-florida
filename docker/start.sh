#!/bin/bash
export ORDINAL_ID=${HOSTNAME##*-} 
export RACK_ID='us-east-'$ORDINAL_ID'b'
envsubst '$RACK_ID' </config/redis_single.yml | tee /config/redis_single.yml
envsubst '${DYNO_TOKEN}' </config/redis_single.yml | tee /config/redis_single.yml
export DYNOMITE_FLORIDA_IP=$(getent hosts floridaservice | awk '{ print $1 }')
dynomite -c /config/dynomite.yml
