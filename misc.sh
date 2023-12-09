oc exec podname -- /bin/bash -c '
if [ -d /path/to/your/folder ]; then
  rm -rf /path/to/your/folder
fi
'
