from kubernetes import client, config
from pprint import pprint
import requests
import os
import time
import redis
import socket



def main():


    DYNOTOKEN = 'DYNO_TOKEN'
    DEFTOKEN = "'3530913378'"
    LOCALHOST = "http://127.0.0.1:22222"
    WRITESONLY = "/state/writes_only"
    LABELSELECTOR = 'app=dynomite,role=worker,token='
    NAMESPACE = "default"
    NORMAL = "NORMAL"
    GETSTATE = "/state/get_state"
    DYNOPORT = ":22222"
    HTTP = "http://"
    RESUMING = "/state/resuming"
    NORMALSTATE = "/state/normal"
    REDISPORT = 22122
    WARMUPSLEEP = 120
    RESUMESLEEP = 15

    config.load_incluster_config()

    v1 = client.CoreV1Api()

    myip = socket.gethostbyname(socket.gethostname())

    localhost = ""


    #we need to know our dynotoken to find our friends!!! :)
    dyno_token = str(os.environ.get(DYNOTOKEN, DEFTOKEN)).replace("'","")


    #this is a warmup script that will bring up a dynomite node
    # first lets put this one in write only
    #this should keep the node from getting read before it is ready

    requests.get(LOCALHOST+WRITESONLY)

    #now we use kubernetes to find a list of nodes with the same token
    list = v1.list_namespaced_pod(NAMESPACE, label_selector=LABELSELECTOR+dyno_token)

    for item in list.items :

        ip = item.status.pod_ip
        # make sure you aren't talking to yourself first dummy!
        if ip in myip:
            continue
        node_state_url = HTTP+ip+DYNOPORT+GETSTATE
        # we walk the list and find a node in "normal" mode, we don't want anyone else that is being warmed up
        state = requests.get(node_state_url)
        if NORMAL in state:
            # we make ourselves a slave of this with redis
            r = redis.StrictRedis(host=myip, port=REDISPORT, decode_responses=True)
            r.slaveof(host=ip, port=REDISPORT)
            # we give that sync a chance to work todo make this configurable with and env variable
            time.sleep(WARMUPSLEEP)
            # now we make ourselves a slave of no one  FREE AT LAST!!!
            r.slaveof(None)

    #now we put ourselves in resuming mode
    requests.get(LOCALHOST+RESUMING)

    #we sleep again for 15 seconds
    time.sleep(RESUMESLEEP)

    #put the node into normal and we are good!
    requests.get(LOCALHOST+NORMALSTATE)



if __name__ == '__main__':
    main()
