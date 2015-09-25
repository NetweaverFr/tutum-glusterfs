# Tutum & GlusterFS

This docker image give you the possibility to create a glusterfs cluster via Tutum.co.

## Constraint:

To have GlusterFs working we based our configuration on some asumptions:
* Glusterfs have to run on a specific cluster on tutum
* Each node of the cluster have to host only one glusterfs container
* GlusterFs have to run on the same service


## Set environemet variables:

To be able to connect to Tutum API you need to pass to environment variable:

| Environment variable     |  Required  | Comment                                       |
|--------------------------|------------|-----------------------------------------------|
| TUTUM_USER               | YES        | Your Tutum username                           |
| TUTUM_APIKEY             | YES        | Your API Key for tutum API                    |
| GLUSTERFS_DEFAULT_VOLUME | NO         | Your Tutum username                           |
