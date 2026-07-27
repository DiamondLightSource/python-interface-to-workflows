import os

import dotenv
from gql import Client, gql
from gql.transport.aiohttp import AIOHTTPTransport
from hera.workflows import Workflow

from python_interface_to_workflows.auth.keycloak_checker import set_token_env_variable


def submit_workflow_to_graphql(w: Workflow):
    yamlstr = w.to_yaml()  # pyright:ignore
    dotenv.load_dotenv(dotenv_path="src/.env", override=True)
    token: str = set_token_env_variable(True)
    host: str = "https://staging.workflows.diamond.ac.uk/graphql"
    visit: str = os.environ.get("NAMESPACE")  # pyright:ignore

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
    result = client.execute(
        mutation,
        variable_values={
            "visit": {
                "proposalCode": str(visit[:2]),
                "proposalNumber": int(visit[2:7]),
                "number": int(visit[-1]),
            },
            "manifest": yamlstr,
        },
    )
    name = str(result["submitWorkflow"]["name"])
    print(f"Job '{name}' submitted to {visit}")
