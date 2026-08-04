import os
import subprocess

import dotenv
from gql import Client, gql
from gql.transport.aiohttp import AIOHTTPTransport
from hera.workflows import Workflow

from python_interface_to_workflows.auth.keycloak_checker import set_token_env_variable


async def submit_workflow(w: Workflow):
    yamlstr = w.to_yaml()  # pyright:ignore
    dotenv.load_dotenv(dotenv_path="src/.env", override=True)
    token: str = set_token_env_variable(True)
    host: str = os.environ.get("HOST")  # pyright:ignore
    visit: str = os.environ.get("VISIT")  # pyright:ignore

    transport = AIOHTTPTransport(
        url=host,
        headers={"Authorization": f"Bearer {token}"},
    )
    client = Client(
        transport=transport,
        fetch_schema_from_transport=True,
    )
    mutation = gql("""
mutation Submit($visit: VisitInput!, $manifest: String!) {
  submitWorkflow(
    visit: $visit
    manifest: $manifest
  ) {
    name
  }
}
""")
    result = await client.execute_async(
        mutation,
        variable_values={
            "visit": {
                "proposalCode": str(visit[:2]),
                "proposalNumber": int(visit[2:7]),
                "number": int(visit[-1]),
            },
            "manifest": f"""{yamlstr}""",
        },
    )
    name = str(result["submitWorkflow"]["name"])
    print(f"Job '{name}' submitted to {visit}")


async def submit_helm(
    w: str,
    chartdir: str = "/workspaces/python-interface-to-workflows/src/python_interface_to_workflows/helm",  # noqa: E501
    filedir: str = "templates",
):
    yamlstr = subprocess.run(
        f"helm template . -s {filedir}/{w}",
        cwd=chartdir,
        shell=True,
        capture_output=True,
        text=True,
    )
    dotenv.load_dotenv(dotenv_path="src/.env", override=True)
    token: str = set_token_env_variable(True)
    host: str = os.environ.get("HOST")  # pyright:ignore
    visit: str = os.environ.get("VISIT")  # pyright:ignore

    transport = AIOHTTPTransport(
        url=host,
        headers={"Authorization": f"Bearer {token}"},
    )
    client = Client(
        transport=transport,
        fetch_schema_from_transport=True,
    )
    mutation = gql("""
mutation Submit($visit: VisitInput!, $manifest: String!) {
  submitWorkflow(
    visit: $visit
    manifest: $manifest
  ) {
    name
  }
}
""")
    result = await client.execute_async(
        mutation,
        variable_values={
            "visit": {
                "proposalCode": str(visit[:2]),
                "proposalNumber": int(visit[2:7]),
                "number": int(visit[-1]),
            },
            "manifest": f"""{yamlstr.stdout}""",
        },
    )
    name = str(result["submitWorkflow"]["name"])
    print(f"Job '{name}' submitted to {visit}")
