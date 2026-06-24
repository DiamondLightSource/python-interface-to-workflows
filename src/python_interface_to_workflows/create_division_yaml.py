import json

from hera.shared import global_config
from hera.workflows import (
    Artifact,
    Steps,
    Volume,
    Workflow,
    script,  # pyright: ignore[reportUnknownVariableType]
)
from hera.workflows import models as m

global_config.host = "https://argo-workflows.staging.workflows.diamond.ac.uk/"
global_config.image = "python:3.10"
global_config.token = "Token"


@script(
    volume_mounts=[m.VolumeMount(name="output-dir", mount_path="/output-dir/")],
    outputs=Artifact(name="json-output", path="/output-dir/output.json"),
)
def do_devision(x: int, y: int):
    div = x / y
    intdiv = x // y
    remain = x % y
    dictionary_of_results = {
        "divide": div,
        "integer divisor": intdiv,
        "remainder": remain,
    }
    with open("/output-dir/output.json", "w") as otpt:
        json.dump(dictionary_of_results, otpt)


with Workflow(
    generate_name="hera-division-",
    entrypoint="divide",
    namespace="ks10000-3",
    name="hera-division",
    api_version="argoproj.io/v1alpha1",
    kind="ClusterWorkflowTemplate",
    labels={"workflows.diamond.ac.uk/science-group-examples": "true"},
    annotations={
        "workflows.argoproj.io/title": "Division via hera test",
        "workflows.argoproj.io/description": """Takes a numerical input and returns the
         remainder, output float, and output string to a json file""",
        "workflows.diamond.ac.uk/repository": "https://github.com/DiamondLightSource/python-interface-to-workflows",
    },
    volumes=Volume(name="output-dir", mount_path="/output-dir", size="1Mi"),
) as w:
    with Steps(name="divide"):
        do_devision(name="first", arguments={"x": 2, "y": 5})


with open("src/divisionyaml.yaml", "w") as div:
    div.write(w.to_yaml())  # pyright: ignore[reportUnknownMemberType]

w.create()
