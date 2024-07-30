POD_NAME="my-pod"
NAMESPACE="default"

# Get the pod's JSON data
POD_JSON=$(oc get pod $POD_NAME --namespace $NAMESPACE -o json)

# Extract creation timestamp
CREATION_TIME=$(echo $POD_JSON | jq -r '.metadata.creationTimestamp')

# Extract container statuses and their start times
CONTAINER_STATUSES=$(echo $POD_JSON | jq -r '.status.containerStatuses')

# Calculate spin-up and init times
for container in $(echo "${CONTAINER_STATUSES}" | jq -r '.[] | @base64'); do
    _jq() {
        echo ${container} | base64 --decode | jq -r ${1}
    }

    CONTAINER_NAME=$(_jq '.name')
    RUNNING_STARTED_AT=$(_jq '.state.running.startedAt')

    if [ ! -z "$RUNNING_STARTED_AT" ]; then
        INIT_TIME=$(date -d "$RUNNING_STARTED_AT" +%s)
        CREATION_TIME_SEC=$(date -d "$CREATION_TIME" +%s)
        INIT_DURATION=$((INIT_TIME - CREATION_TIME_SEC))
        echo "Container $CONTAINER_NAME init time: $INIT_DURATION seconds"
    fi
done
