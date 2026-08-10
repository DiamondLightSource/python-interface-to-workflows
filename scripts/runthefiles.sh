#!/bin/bash
cd src/python_interface_to_workflows/workflow_definitions
for file in *
do
[[ -d "$file" ]] && continue
    if grep -Eq '^\s*(from|import)\s+python_workflow_submitter\b' "$file"; then
        echo "ERROR: $file imports submitter"
        exit 1
    fi
uv run "$file"
done
if compgen -G "*.yaml" > /dev/null || compgen -G "*.txt" > /dev/null; then
    mv -- *.yaml *.txt ../templates/
    git add ../templates/
fi
