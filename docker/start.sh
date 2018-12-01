#!/bin/bash
cd /dynomiteconfig
wget https://raw.githubusercontent.com/ibivibiv/dynomite-florida/master/dynomite_single.yml
python alpha_parse.py
envsubst '$RACK_ID' </dynomiteconfig/dynomite_single.yml | tee /dynomiteconfig/dynomite_single.yml
envsubst '${DYNO_TOKEN}' </dynomiteconfig/dynomite_single.yml | tee /dynomiteconfig/dynomite_single.yml
mv /dynomiteconfig/dynomite_single.yml /etc/dynomitedb/dynomite.yaml
export DYNOMITE_FLORIDA_IP=$(getent hosts floridaservice | awk '{ print $1 }')
dynomite -c /etc/dynomitedb/dynomite.yaml

