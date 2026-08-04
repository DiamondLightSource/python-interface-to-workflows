import json

from hera.shared import global_config
from hera.workflows import (
    DAG,
    Artifact,
    Script,
    Volume,
    Workflow,
    script,  # pyright: ignore[reportUnknownVariableType]
)
from hera.workflows import models as m
from hera.workflows.archive import NoneArchiveStrategy

global_config.set_class_defaults(  # pyright: ignore
    Script,
    image="ghcr.io/matt-carre/python-interface-to-workflows-mounted-image:latest",
)


@script(
    command=["python"],
    outputs=Artifact(
        name="notebook", path="/tmp/notebook.html", archive=NoneArchiveStrategy()
    ),
    volume_mounts=[m.VolumeMount(name="tmpdir", mount_path="/tmp")],
)
def mount_files():
    import subprocess

    subprocess.call("python -m venv /tmp/venv", shell=True)
    subprocess.call(
        "/tmp/venv/bin/pip install -r /mounted_files/requirements.txt", shell=True
    )
    subprocess.call(
        "/tmp/venv/bin/python -m ipykernel install --prefix=/tmp/venv --name=venv",
        shell=True,
    )
    subprocess.call(
        "/tmp/venv/bin/python -m jupyter nbconvert --execute --allow-errors --to html --output notebook --output-dir /tmp /mounted_files/notebook.ipynb",  # noqa: E501
        shell=True,
    )


with Workflow(
    pod_spec_patch=json.dumps(
        {
            "containers": [
                {
                    "name": "main",
                    "resources": {
                        "limits": {
                            "cpu": "500m",
                            "memory": "2Gi",
                        },
                        "requests": {
                            "cpu": "500m",
                            "memory": "2Gi",
                        },
                    },
                }
            ]
        }
    ),
    tolerations=[
        m.Toleration(
            key="nodetype", operator="Equal", value="gpu", effect="NoSchedule"
        ),
        m.Toleration(
            key="nodegroup", operator="Equal", value="workflows", effect="NoSchedule"
        ),
    ],
    name="hera-example-pandas",
    entrypoint="workflowentry",
    api_version="argoproj.io/v1alpha1",
    kind="WorkflowTemplate",
    labels={"workflows.diamond.ac.uk/science-group-examples": "true"},
    annotations={
        "workflows.argoproj.io/title": "notebook.yaml remade via hera",
        "workflows.argoproj.io/description": """Replicates the functionality of
notebook.yaml""",
        "workflows.diamond.ac.uk/repository": "https://github.com/DiamondLightSource/python-interface-to-workflows",
    },
    volumes=Volume(name="tmpdir", mount_path="/tmp/", size="1Gi"),
) as w:
    with DAG(name="workflowentry"):
        files = mount_files()
        files  # pyright: ignore # noqa: B018


with open(
    "src/python_interface_to_workflows/templates/example_import_files.txt", "w"
) as div:
    div.write(w.to_yaml())  # pyright: ignore[reportUnknownMemberType]
