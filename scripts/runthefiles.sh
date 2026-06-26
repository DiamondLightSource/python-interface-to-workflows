#!/bin/bash
cd src/python_interface_to_workflows/workflow_definitions
for file in *
do
uv run "$file"
done
mv *.yaml ../templates/
git add -u ../templates/
