#!/bin/bash
cd src/python_interface_to_workflows/templates
for file in *.txt; do
    yaml_file="${file}.yaml"

    mv "$file" "$yaml_file"
    argo lint "$yaml_file" --offline
    mv "$yaml_file" "$file"
done
exit 0
