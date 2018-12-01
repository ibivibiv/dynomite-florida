from kubernetes import client, config
import requests
import os
import time
import redis
import socket
import logging
import sys


def main():

    #let's get some literals set up that need to be in a config mechanism later
    DYNOTOKEN = 'DYNO_TOKEN'
    PODNAME = 'POD_NAME'
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
    STARTUPSLEEP = 60
    WARMUPSLEEP = 120
    RESUMESLEEP = 15

    #time for some logging that will help make the console logs visible in pod logs for debug
    root = logging.getLogger()
    root.setLevel(logging.DEBUG)

    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    root.addHandler(ch)


    # the label for status is set to standby so we shouldn't be visible in the service just yet

    # this is so cheating but lets let dynomite at least start up first
    logging.info("sleeping")
    time.sleep(STARTUPSLEEP)

    try:

        config.load_incluster_config()

        v1 = client.CoreV1Api()

        logging.info("built client")

        myip = socket.gethostbyname(socket.gethostname())

        logging.info("got ip")
        localhost = ""

        # we need to know our dynotoken to find our friends!!! :)
        dyno_token = str(os.environ.get(DYNOTOKEN, DEFTOKEN)).replace("'", "")
        pod_name = os.environ.get(PODNAME)
        logging.info("got pod name")
        # this is a warmup script that will bring up a dynomite node
        # first lets put this one in write only
        # this should keep the node from getting read before it is ready

        #requests.get(LOCALHOST + WRITESONLY)

        logging.info("set write only")

        # now we use kubernetes to find a list of nodes with the same token
        list = v1.list_namespaced_pod(NAMESPACE, label_selector=LABELSELECTOR + dyno_token)

        logging.info("got list "+str(len(list.items)))

        for item in list.items:

            ip = item.status.pod_ip
            logging.info("got ip "+ip)
            # make sure you aren't talking to yourself first dummy!
            if ip in myip:
                continue
            node_state_url = HTTP + ip + DYNOPORT + GETSTATE
            logging.info("node state url "+node_state_url)

            # TODO I bet we need to ping this first to make sure it is even healthy first

            # we walk the list and find a node in "normal" mode, we don't want anyone else that is being warmed up
            state = requests.get(node_state_url)

            logging.info("got state ")

            if NORMAL in state:
                # we make ourselves a slave of this with redis
                r = redis.StrictRedis(host=myip, port=REDISPORT, decode_responses=True)
                logging.info('got redis client')

                info = r.info()

                logging.info('got info')

                keycount = int(info['db0']['keys'])

                logging.info('got keycount'+str(keycount))
                #we don't care about empty nodes
                if keycount <= 0 :
                    continue

                r.slaveof(host=ip, port=REDISPORT)
                logging.info('set slave of '+ip)
                # we give that sync a chance to work and there needs to be a better way to do this but I researched and No for now
                time.sleep(WARMUPSLEEP)
                # now we make ourselves a slave of no one  FREE AT LAST!!!
                r.slaveof(None)
                logging.info("redis replicated")

        # now we put ourselves in resuming mode
        #requests.get(LOCALHOST + RESUMING)

        logging.info("set resuming")

        # we sleep again for 15 seconds
        time.sleep(RESUMESLEEP)

        # put the node into normal and we are good!
        #requests.get(LOCALHOST + NORMALSTATE)

        logging.info("set to normal")

        v1.patch_namespaced_pod(name=pod_name, namespace=NAMESPACE, body=[{
            "op": "add", "path": "/metadata/labels/status", "value": "running"
        }])

        logging.info("set the pod data to running")

    except Exception, e:
        logging.info(str(e))
        exit(1)


    while True:
        time.sleep(6000)


    exit(0)


if __name__ == '__main__':
    main()
