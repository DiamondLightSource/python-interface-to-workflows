from gql import Client, gql
from gql.transport.aiohttp import AIOHTTPTransport


def submit_to_graphql():
    transport = AIOHTTPTransport(
        url="https://staging.workflows.diamond.ac.uk/graphql",
        headers={"Authorization": "Bearer "},  # after Bearer = access token
    )
    client = Client(
        transport=transport,
        fetch_schema_from_transport=True,
    )
    mutation = gql("""
mutation SubmitDivision {
  submitWorkflowTemplate(
    name: "divisionyaml.yaml"
    visit: {
      proposalCode: "ks",
      proposalNumber: 10000,
      number: 3
    }
     parameters: {
       x: "19",
       y: "10"
     }
    ){
    name
}
}
""")
    result = client.execute(mutation)
    visit = "ks10000-3/c"
    name = str(result["submitWorkflowTemplate"]["name"])
    print(f"Job '{visit}-{name}' submitted.")


submit_to_graphql()
