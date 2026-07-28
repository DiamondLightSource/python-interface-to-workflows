#!/bin/bash
cd src/python_interface_to_workflows/workflow_definitions
for file in *
do
[[ -d "$file" ]] && continue
uv run "$file"
done
mv *.txt ../templates/
git add -u ../templates/
