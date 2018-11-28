#!/bin/bash
cd /dynomiteconfig
wget https://raw.githubusercontent.com/ibivibiv/dynomite-florida/master/dynomite_single.yml
python alpha_parse.py
mv /dynomiteconfig/dynomite_single.yml /config/dynomite.yml
export DYNOMITE_FLORIDA_IP=$(getent hosts floridaservice | awk '{ print $1 }')
dynomite -c /config/dynomite.yml 

