import tutum
import os
import subprocess
import time
import re
from time import sleep

command = ['glusterd']
subprocess.Popen(command)

while True:
    # Set variables
    # Service name
    serviceName = os.environ.get('TUTUM_SERVICE_HOSTNAME')
    # Default volume
    if os.environ.get('GLUSTERFS_DEFAULT_VOLUME_NAME'):
        defaultVolume = os.environ.get('GLUSTERFS_DEFAULT_VOLUME_NAME')
    else:
        defaultVolume = 'glusterfs/data'

    # Get the right service
    services = tutum.Service.list(state = 'Running', name = serviceName)

    # Check result - we want only one service
    if services.__len__() == 1:
        service = services[0]
        # Get container list
        containers = tutum.Container.list(state = 'Running', serviceName = serviceName)

        # If we have more than one container running GlusterFs
        # We can create/update the cluster
        if containers.__len__() > 1:

            # get peers informations
            command = ['gluster', 'peer', 'status']
            statePeer = subprocess.Popen(command, stderr=subprocess.STDOUT)
            # get the peer response with the peers IP
            stdout = statePeer.stdout.read()

            for container in containers:
                peer = re.match(container.__getattribute__('private_ip'), stdout)

                if not peer:
                    command = ['gluster', 'peer', 'probe', container.__getattribute__('private_ip')]
                    statePeer = subprocess.Popen(command)

            # Check if a volume is set
            command = ['gluster', 'volume', 'info']
            stateVolume = subprocess.Popen(command)

    elif services.__len__() > 1:
        print "More than one service found for " + serviceName
    else:
        print "No service found - " + serviceName

    # List all container:
    sleep(20)
