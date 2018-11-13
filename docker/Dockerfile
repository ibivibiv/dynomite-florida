#Download base image from known working dyomite conductor image
FROM v1r3n/dynomite
 
# Update Software repository
RUN apt-get update

#install libraries
RUN apt-get install -y sudo gnupg2 curl wget

#add repo for nodejs
RUN curl -sL https://deb.nodesource.com/setup_10.x | sudo -E bash -

#install nodejs
RUN apt-get install -y nodejs

#install express and proxy middle
RUN npm install express
RUN npm install http-proxy-middleware

#set the environment variables for Florida.  If you want to use Florida directly instead of the proxy below then you change these to match your installation
ENV DYNOMITE_FLORIDA_PORT=8080
ENV DYNOMITE_FLORIDA_IP="127.0.0.1"

#get the node-proxy if you don't want to use the local proxy then comment this one out and change the start.sh as well to not start it
RUN wget https://raw.githubusercontent.com/ibivibiv/conductor-configs/master/proxy.js

#set up the config 
RUN mkdir /dynomiteconfig
RUN cd /dynomiteconfig && wget <your redis_florida.yml location here>
RUN mv /dynomiteconfig/redis_florida.yml /dynomite/conf/redis_single.yml

# Configure Services and Port
COPY start.sh /dynomite/startup.sh

##################### INSTALLATION ENDS #####################

# Expose the peer port
RUN echo 'Exposing peer port 8101'
EXPOSE 8103

# Expose the underlying Redis port
RUN echo 'Exposing Redis port 22122'
EXPOSE 22123

# Expose the stats/admin port
RUN echo 'Exposing stats/admin port 22222'
EXPOSE 22223

# Default port to acccess Dynomite
RUN echo 'Exposing client port for Dynomite 8102'
EXPOSE 8104


# Setting overcommit for Redis to be able to do BGSAVE/BGREWRITEAOF
RUN sysctl vm.overcommit_memory=1
