#!/bin/python
import os
import re

import yaml

yamlpath = "src/python_interface_to_workflows/templates/"
yamllist: list[str] = []
for x in os.listdir(yamlpath):
    if x.endswith(".yaml"):
        yamllist.append(x)

for file in yamllist:
    metadata = api_ver = clst_tmpt = title = repo = group = annotations = labels = False
    with open(yamlpath + file) as s:
        yamldata = yaml.load(s, Loader=yaml.FullLoader)
    if "apiVersion" in yamldata.keys():
        match yamldata["apiVersion"]:
            case "argoproj.io/v1alpha1":
                api_ver = True
            case _:
                api_ver = False
    else:
        api_ver = False
    if "kind" in yamldata.keys():
        match yamldata["kind"]:
            case "Workflow":
                clst_tmpt = True
            case _:
                clst_tmpt = False
    else:
        clst_tmpt = False
    if "metadata" in yamldata.keys() and type(yamldata["metadata"]) is dict:
        normal_name = False
        gen_name = False
        if "generateName" in yamldata["metadata"].keys():
            gen_name = True
        if "name" in yamldata["metadata"].keys():
            normal_name = True
        if "annotations" in yamldata["metadata"].keys():
            annotations = True
            if (
                "workflows.argoproj.io/title"
                in yamldata["metadata"]["annotations"].keys()
            ):
                title = True
            else:
                title = False
            if (
                "workflows.diamond.ac.uk/repository"
                in yamldata["metadata"]["annotations"].keys()
            ):
                repo = True
            else:
                repo = False
        else:
            annotations = title = repo = False
        if "labels" in yamldata["metadata"].keys():
            labels = True
            if yamldata["metadata"]["labels"]:
                group = any(
                    re.match(r"workflows.diamond.ac.uk/science-group-.+", d)
                    for d in yamldata["metadata"]["labels"].keys()
                )
            else:
                group = False
        else:
            group = labels = False
    else:
        metadata = normal_name = gen_name = False
    if api_ver and clst_tmpt and title and repo and group and annotations and labels:
        if gen_name != normal_name:
            exit(0)
        else:
            print(
                "generated_name and normal_name error, must have one of these not both"
            )
            exit(1)
    else:
        print(f"""
                metadata present?: {metadata}
                annotations present?: {annotations}
                labels present?: {labels}
                api_ver present?: {api_ver}
                cluster template present?: {clst_tmpt}
                title present?: {title}
                repository present?: {repo}
                group present?: {group}""")
        exit(1)
