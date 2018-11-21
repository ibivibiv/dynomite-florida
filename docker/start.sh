#!/bin/bash
export ORDINAL_ID=${HOSTNAME##*-} 
export ORDINAL_LETTER=$(python alpha_parse.py $ORDINAL_ID)
export RACK_ID='us-east-1'$ORDINAL_LETTER
envsubst '$RACK_ID' </config/dynomite_single.yml | tee /config/dynomite_single.yml
#envsubst '${DYNO_TOKEN}' </config/redis_single.yml | tee /config/redis_single.yml
export DYNOMITE_FLORIDA_IP=$(getent hosts floridaservice | awk '{ print $1 }')
dynomite -c /config/dynomite.yml -g
