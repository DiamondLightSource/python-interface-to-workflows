#!/bin/bash
cd src/python_interface_to_workflows/templates
for file in *
do
argo lint "$file" --offline
SUCCESSFULLINT=$?
[ $SUCCESSFULLINT -ne 0 ] && exit 1
done
exit 0
