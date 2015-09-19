import tutum
import os
import subprocess
import time

from daemons import daemonizer

@daemonizer.run(pidfile="/tmp/glusterFsAutoDiscovery.pid")

def glusterFsAutoDiscovery(sleep_time):

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

                # Check if a peer is set
                command = ['gluster', 'peer', 'status']
                statePeer = subprocess.Popen(command)

                # If a peer is set so the cluster is ok
                if statePeer.wait() == 1:
                    print 'One peer.'
                else:
                    for container in containers:
                        command = ['gluster', 'peer', 'probe', container.__getattribute__('private_ip')]
                        statePeer = subprocess.Popen(command)

                # Check if a volume is set
                command = ['gluster', 'volume', 'info']
                stateVolume = subprocess.Popen(command)


                if stateVolume.wait() == 1:
                    print "plop"

        elif services.__len__() > 1:
            print "More than one service found for " + serviceName
        else:
            print "No service found - " + serviceName

        # List all container:

sleep(20)
