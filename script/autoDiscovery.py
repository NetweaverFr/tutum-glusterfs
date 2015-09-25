import os
import re
import subprocess
import time
import tutum
import unicodedata

from time import sleep

class autoDiscovery(object):
    """A class that manage auto discovery for Glusterfs/Docker/Tutum cluster."""

    def __init__(self, volumeDefault = None, daemon ='glusterd'):
        # Set variables
        self.serviceName = os.environ.get('TUTUM_SERVICE_HOSTNAME')
        self.serviceRunning = 0
        self.containersRunning = 0
        self.volumeDefault = volumeDefault
        self.glusterfsDaemon = daemon
        self.commandCreateVolume = []
        print "Variable setup"

        # Set default volume
        if self.volumeDefault == None:
            if os.environ.get('GLUSTERFS_DEFAULT_VOLUME'):
                self.volumeDefault = os.environ.get('GLUSTERFS_DEFAULT_VOLUME')
            else:
                self.volumeDefault = "data"

        print "Default volume path setup (" + self.volumeDefault + ")."

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
            #self.commandCreateVolume.append(str(container.__getattribute__('private_ip')) + ':' + defaultVolume)
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
        command = [self.glusterfsDaemon]
        subprocess.Popen(command)

        while True:
            # Get the gluster service
            services = tutum.Service.list(state = 'Running', name = self.serviceName)
            self.serviceRunning = services.__len__();

            # Check if we have only one service
            if self.serviceRunning == 1:
                print self.serviceName + " found."

                # Get container list
                containers = tutum.Container.list(state = 'Running', serviceName = self.serviceName)
                self.containersRunning = containers.__len__()
                # If we have more than one container running GlusterFs
                # We can create/update the cluster
                if self.containersRunning > 1:

                    print containers.__len__() + ' Containers currently running'
                    print containers
                    #preset command to create volume
                    #self.commandCreateVolume = ['gluster', 'volume', 'create', 'volume1', 'replica', self.containersRunning, 'transport', 'tcp']

                    self.peer(containers)

                    # Check if a volume is set
                    command = ['gluster', 'volume', 'info']
                    stateVolume = subprocess.Popen(command)

                    #self.commandCreateVolume.append('force')
                    #createVolume = subprocess.Popen    self.commandCreateVolume)
                    #createVolume = subprocess.Popen(['gluster', 'volume', 'start', 'volume1'])

                elif services.__len__() > 1:
                    print "More than one service found for " + self.serviceName
                else:
                    print "No service found - " + self.serviceName

            sleep(20)


adScript = autoDiscovery()
adScript.execute()
