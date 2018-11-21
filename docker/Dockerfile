#Download base image from known working dyomite conductor image
#FROM gleam/dynomite
FROM v1r3n/dynomite

# Update Software repository
#RUN apt-key adv --keyserver keyserver.ubuntu.com --recv-keys FB3291D9
#RUN add-apt-repository "deb https://apt.dynomitedb.com/ trusty main"
RUN apt-get update

#install libraries
RUN apt-get install -y sudo gnupg2 curl wget 


#set up the config 
RUN mkdir /dynomiteconfig
RUN mkdir /config
RUN wget https://raw.githubusercontent.com/ibivibiv/dynomite-florida/master/alpha_parse.py
RUN cd /dynomiteconfig && wget https://raw.githubusercontent.com/ibivibiv/dynomite-florida/master/dynomite_single.yml
RUN mv /dynomiteconfig/dynomite_single.yml /config/dynomite.yml

# Configure Services and Port
COPY start.sh /start.sh
RUN chmod 755 /start.sh
ENTRYPOINT ["/start.sh"]


##################### INSTALLATION ENDS #####################

# Expose the peer port
RUN echo 'Exposing peer port 8101'
EXPOSE 8101

# Expose the underlying Redis port
RUN echo 'Exposing Redis port 22122'
EXPOSE 22122

# Expose the stats/admin port
RUN echo 'Exposing stats/admin port 22222'
EXPOSE 22222

# Default port to acccess Dynomite
RUN echo 'Exposing client port for Dynomite 8102'
EXPOSE 8102
