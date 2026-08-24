[![CI](https://github.com/DiamondLightSource/python-interface-to-workflows/actions/workflows/ci.yml/badge.svg)](https://github.com/DiamondLightSource/python-interface-to-workflows/actions/workflows/ci.yml)
[![Coverage](https://codecov.io/gh/DiamondLightSource/python-interface-to-workflows/branch/main/graph/badge.svg)](https://codecov.io/gh/DiamondLightSource/python-interface-to-workflows)

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://www.apache.org/licenses/LICENSE-2.0)

# python_interface_to_workflows

 Python alternative to creating and running argo workflows in the Data Analysis Platform

This provides a copier template and demonstrating how to use Hera to rewrite workflows using python.

What            | Where
:---:           | :---:
Source          | <https://github.com/DiamondLightSource/python-interface-to-workflows>
Docker          | `docker run ghcr.io/diamondlightsource/python-interface-to-workflows:latest`
Releases        | <https://github.com/DiamondLightSource/python-interface-to-workflows/releases>


# Examples
What            | Where
:---:           | :---:
A basic example showing a file being mounted from a folder and a notebook running in a pod | <https://github.com/DiamondLightSource/python-interface-to-workflows/blob/main/src/python_interface_to_workflows/workflow_definitions/create_notebook_in_image.py>
A more advanced example showing a visr recon workflow, converting an .nxs to a .hdf5 file.          | <https://github.com/DiamondLightSource/python-interface-to-workflows/blob/main/src/python_interface_to_workflows/workflow_definitions/visr_notebook_example/visr-recon.ipynb>
# Using Copier
```bash
module load uv
mkdir new_directory_path
cd new_directory_path
git init 
git remote add origin {origin ssh}
git branch -M main

cd ..
```
then either:
```bash
git clone git@github.com:DiamondLightSource/python-interface-to-workflows.git
uvx copier copy {this_repo's_path} {new_directory_path}
```
or:
```bash
uvx copier copy git@github.com:DiamondLightSource/python-interface-to-workflows.git .
code .
```

Then:
1) create a .env file in src
2) run uv lock
3) rebuild and reopen in container

To submit your yaml files in a notebook, append the following:

```python
from python_workflow_submitter.submit_workflow import submit_workflow_yaml

await submit_workflow_yaml("example.yaml")
```

Alternatively:
```python
import asyncio
import os

from python_workflow_submitter.submit_workflow import submit_workflow_yaml

asyncio.run(submit_workflow_yaml("example.yaml", visit=os.environ.get("VISIT")))
```
