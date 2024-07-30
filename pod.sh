#!/bin/bash

POD_NAME="my-pod"
NAMESPACE="default"

# Get pod's JSON data
POD_JSON=$(oc get pod $POD_NAME --namespace $NAMESPACE -o json)

# Extract creation timestamp
CREATION_TIME=$(echo $POD_JSON | jq -r '.metadata.creationTimestamp')

# Get pod events
EVENTS_JSON=$(oc get events --namespace $NAMESPACE --field-selector involvedObject.name=$POD_NAME -o json)

# Extract scheduled time from events
SCHEDULED_TIME=$(echo $EVENTS_JSON | jq -r '.items[] | select(.reason=="Scheduled") | .firstTimestamp')

# Extract container statuses
CONTAINER_STATUSES=$(echo $POD_JSON | jq -r '.status.containerStatuses')

# Initialize variables
TOTAL_INIT_TIME=0
POD_RUNNING_TIME=0
CONTAINER_COUNT=0
RUNNING_TIME=0

for container in $(echo "${CONTAINER_STATUSES}" | jq -r '.[] | @base64'); do
    _jq() {
        echo ${container} | base64 --decode | jq -r ${1}
    }

    CONTAINER_NAME=$(_jq '.name')
    RUNNING_STARTED_AT=$(_jq '.state.running.startedAt')

    if [ ! -z "$RUNNING_STARTED_AT" ]; then
        START_TIME_SEC=$(date -d "$RUNNING_STARTED_AT" +%s)
        CREATION_TIME_SEC=$(date -d "$CREATION_TIME" +%s)
        INIT_TIME=$((START_TIME_SEC - CREATION_TIME_SEC))
        TOTAL_INIT_TIME=$((TOTAL_INIT_TIME + INIT_TIME))
        CONTAINER_COUNT=$((CONTAINER_COUNT + 1))
        if [ $START_TIME_SEC -gt $RUNNING_TIME ]; then
            RUNNING_TIME=$START_TIME_SEC
        fi
    fi
done

if [ $CONTAINER_COUNT -gt 0 ]; then
    # Calculate total times
    CREATION_TIME_SEC=$(date -d "$CREATION_TIME" +%s)
    SCHEDULED_TIME_SEC=$(date -d "$SCHEDULED_TIME" +%s)
    TOTAL_TIME=$((RUNNING_TIME - SCHEDULED_TIME_SEC))
    SPIN_UP_TIME=$((RUNNING_TIME - CREATION_TIME_SEC))
    INIT_TIME_AVG=$((TOTAL_INIT_TIME / CONTAINER_COUNT))

    # Output results
    echo "Scheduled Time to Create Time: $((CREATION_TIME_SEC - SCHEDULED_TIME_SEC)) seconds"
    echo "Pod Spin-Up Time: $SPIN_UP_TIME seconds"
    echo "Average Container Init Time: $INIT_TIME_AVG seconds"
    echo "Total Time (Scheduled to Running): $TOTAL_TIME seconds"
else
    echo "No running container start times found."
fi
