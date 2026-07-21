#!/bin/bash
cd "src/python_interface_to_workflows/workflow_definitions"

cp *example*.py "../../copier_template/src/{{ project_name }}/workflow_definitions"
cp ../templates/*.yaml "../../copier_template/src/{{ project_name }}/templates"

for file in "../../copier_template/src/{{ project_name }}/workflow_definitions"/*
do
    [[ $file == *.jinja ]] && continue
    sed -i 's/python-interface-to-workflows/{{repo_name}}/g' "$file"
    sed -i 's/DiamondLightSource/{{github_org}}/g' "$file"
    mv "$file" "$file.jinja"
done

for file in "../../copier_template/src/{{ project_name }}/templates"/*
do
    [[ $file == *.jinja ]] && continue
    sed -i 's/python-interface-to-workflows/{{repo_name}}/g' "$file"
    sed -i 's/DiamondLightSource/{{github_org}}/g' "$file"
    mv "$file" "$file.jinja"
done
git add "../../copier_template/src/{{ project_name }}/workflow_definitions"/*
git add "../../copier_template/src/{{ project_name }}/templates"/*
