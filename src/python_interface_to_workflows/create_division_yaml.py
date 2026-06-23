import json

from hera.workflows import (
    Artifact,
    Steps,
    Volume,
    Workflow,
    WorkflowsService,
    script,  # pyright: ignore[reportUnknownVariableType]
)
from hera.workflows import models as m


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
    generate_name="hera-division",
    entrypoint="divide",
    namespace="https://staging.workflows.diamond.ac.uk/workflows/",
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

sendthis = m.WorkflowSubmitRequest(
    namespace="https://staging.workflows.diamond.ac.uk/workflows/",
    resource_kind="ClusterWorkflowTemplate",
    resource_name="hera-division",
)
a = WorkflowsService(
    host="https://staging.workflows.diamond.ac.uk/graphql",
    namespace="https://staging.workflows.diamond.ac.uk/workflows/",
    token="a",
)
WorkflowsService.submit_workflow(a, req=sendthis)
