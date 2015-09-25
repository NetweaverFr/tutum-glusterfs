import os
import re
import subprocess
import time
import tutum
import unicodedata

from time import sleep

class autoDiscovery():
    """A class that manage auto discovery for Glusterfs/Docker/Tutum cluster."""

    def __init__(volumeDefault = null, daemon = 'glusterd'):
        # Set variables
        self.service.name = os.environ.get('TUTUM_SERVICE_HOSTNAME')
        self.service.running = 0
        self.containers.running = 0
        self.volume.default = volumeDefault
        self.glusterfs.daemon = daemon

        # Set default volume
        if self.volume.default == null:
            self.volume.default = os.environ.get('GLUSTERFS_DEFAULT_VOLUME')

    def peer(self, containers):
        # get peers informations
        command = ['gluster', 'peer', 'status']
        statePeer = subprocess.Popen(command, stdout=subprocess.PIPE)
        # get the peer response with the peers IP
        stdout = statePeer.communicate()[0]
        print stdout
        
        # Check each container
        for container in containers:
            # Add container for volume creation
            commandCreateVolume.append(str(container.__getattribute__('private_ip')) + ':' + defaultVolume)
            # Check if the container is not the same as the one who execute this script
            if not re.search(container.__getattribute__('private_ip'), os.environ.get('TUTUM_IP_ADDRESS')):
                # Search if the container is in the peer list
                peer = re.search(container.__getattribute__('private_ip'), stdout)
                # If not we add the peer
                if not peer:
                    command = ['gluster', 'peer', 'probe', container.__getattribute__('private_ip')]
                    statePeer = subprocess.Popen(command)

    def execute(self):
        # Execute Glusterfs Daemon
        command = [self.glusterfs.daemon]
        subprocess.Popen(command)

        # Get the gluster service
        services = tutum.Service.list(state = 'Running', name = self.service.name)
        self.service.running = services.__len__();

        # Check if we have only one service
        if self.service.running == 1:
            print self.service.name + " found."
            while True:
                # Get container list
                containers = tutum.Container.list(state = 'Running', serviceName = self.service.name)
                self.containers.running = containers.__len__()
                # If we have more than one container running GlusterFs
                # We can create/update the cluster
                if self.containers.running > 1:

                    #preset command to create volume
                    commandCreateVolume = ['gluster', 'volume', 'create', 'volume1', 'replica', self.containers.running, 'transport', 'tcp']

                    self.peer(containers)

                    # Check if a volume is set
                    command = ['gluster', 'volume', 'info']
                    stateVolume = subprocess.Popen(command)

                    #commandCreateVolume.append('force')
                    #createVolume = subprocess.Popen(commandCreateVolume)
                    #createVolume = subprocess.Popen(['gluster', 'volume', 'start', 'volume1'])

            elif services.__len__() > 1:
                print "More than one service found for " + self.service.name
            else:
                print "No service found - " + self.service.name

            # List all container:
            sleep(20)


adScript = autoDiscovery()
adScript.execute()
