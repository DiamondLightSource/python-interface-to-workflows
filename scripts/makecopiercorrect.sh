#!/bin/bash
cd "src/python_interface_to_workflows/workflow_definitions"

cp *example*.py "../../copier_template/src/{{ project_name }}/workflow_definitions"
cp ../templates/*example*.txt "../../copier_template/src/{{ project_name }}/templates"

for file in "../../copier_template/src/{{ project_name }}/workflow_definitions"/*
do
    [[ -d "$file" ]] && continue
    [[ $file == *.jinja ]] && continue

    sed -i 's/python-interface-to-workflows/{{repo_name}}/g' "$file"
    sed -i 's/DiamondLightSource/{{github_org}}/g' "$file"
    sed -i 's/python_interface_to_workflows/{{project_name}}/g' "$file"

    sed -i '1i{% raw %}' "$file"
    echo '{% endraw %}' >> "$file"

    sed -i \
        -e 's/{{repo_name}}/{% endraw %}{{repo_name}}{% raw %}/g' \
        -e 's/{{github_org}}/{% endraw %}{{github_org}}{% raw %}/g' \
        -e 's/{{project_name}}/{% endraw %}{{project_name}}{% raw %}/g' \
        "$file"

    mv "$file" "$file.jinja"
done
for file in "../../copier_template/src/{{ project_name }}/workflow_definitions/notebooks"/*
do
    [[ -d "$file" ]] && continue
    [[ $file == *.jinja ]] && continue

    sed -i 's/python-interface-to-workflows/{{repo_name}}/g' "$file"
    sed -i 's/DiamondLightSource/{{github_org}}/g' "$file"

    sed -i 's/python_interface_to_workflows/{{project_name}}/g' "$file"
    sed -i '1i{% raw %}' "$file"
    echo '{% endraw %}' >> "$file"

    sed -i \
        -e 's/{{repo_name}}/{% endraw %}{{repo_name}}{% raw %}/g' \
        -e 's/{{github_org}}/{% endraw %}{{github_org}}{% raw %}/g' \
        -e 's/{{project_name}}/{% endraw %}{{project_name}}{% raw %}/g' \
        "$file"


    mv "$file" "$file.jinja"
done
for file in "../../copier_template/src/{{ project_name }}/templates"/*
do
    [[ -d "$file" ]] && continue
    [[ $file == *.jinja ]] && continue

    sed -i 's/python-interface-to-workflows/{{repo_name}}/g' "$file"
    sed -i 's/DiamondLightSource/{{github_org}}/g' "$file"
    sed -i 's/python_interface_to_workflows/{{project_name}}/g' "$file"
    sed -i '1i{% raw %}' "$file"
    echo '{% endraw %}' >> "$file"

    sed -i \
        -e 's/{{repo_name}}/{% endraw %}{{repo_name}}{% raw %}/g' \
        -e 's/{{github_org}}/{% endraw %}{{github_org}}{% raw %}/g' \
        -e 's/{{project_name}}/{% endraw %}{{project_name}}{% raw %}/g' \
        "$file"

    mv "$file" "$file.jinja"
done
git add "../../copier_template/src/{{ project_name }}/workflow_definitions"/*
git add "../../copier_template/src/{{ project_name }}/templates"/*
