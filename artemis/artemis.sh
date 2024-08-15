#!/bin/bash
# This script is used to run the artemis MQ broker in a container

# define these variables before running the script
#export POD_CONTAINER = podman | docker

# If a .env file is present, it will read the environment variables from there
# The .env file should be in the same directory as the script
# Rename the .env.example file to .env and set the environment variables
if [ -f ./.env ]; then
	. ./.env
fi

echo "Pod container: $POD_CONTAINER"

MOUNT_ETC_OVERRIDE=""
if [ "$1" == "--disable-persistence" ]; then
  echo "Disabling persistence"
  MOUNT_ETC_OVERRIDE="-v ${PWD}/etc-override:/var/lib/artemis-instance/etc-override"
fi

set -x
$POD_CONTAINER run --rm --name mycontainer -p 61616:61616 -p 8161:8161 ${MOUNT_ETC_OVERRIDE} --rm apache/activemq-artemis:latest-alpine
set +x