import os
import re
import subprocess
import time
import tutum
import unicodedata

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

        #preset command to create volume
        commandCreateVolume = ['gluster', 'volume', 'create', 'volume1', 'replica', str(containers.__len__()), 'transport', 'tcp']

        # If we have more than one container running GlusterFs
        # We can create/update the cluster
        if containers.__len__() > 1:
            # get peers informations
            command = ['gluster', 'peer', 'status']
            statePeer = subprocess.Popen(command, stdout=subprocess.PIPE)
            # get the peer response with the peers IP
            stdout = statePeer.communicate()[0]

            # Check each container
            for container in containers:

                # Add container for volume creation
                commandCreateVolume.append(str(container.__getattribute__('private_ip')) + ':/data')

                # Check if the container is not the same as the one who execute this script
                if not re.search(container.__getattribute__('private_ip'), os.environ.get('TUTUM_IP_ADDRESS')):
                    # Search if the container is in the peer list
                    peer = re.search(container.__getattribute__('private_ip'), stdout)
                    # If not we add the peer
                    if not peer:
                        command = ['gluster', 'peer', 'probe', container.__getattribute__('private_ip')]
                        statePeer = subprocess.Popen(command)

            # Check if a volume is set
            command = ['gluster', 'volume', 'info']
            stateVolume = subprocess.Popen(command)

            commandCreateVolume.append('force')
            createVolume = subprocess.Popen(commandCreateVolume)
            createVolume = subprocess.Popen(['gluster', 'volume', 'start', 'volume1'])

    elif services.__len__() > 1:
        print "More than one service found for " + serviceName
    else:
        print "No service found - " + serviceName

    # List all container:
    sleep(20)
