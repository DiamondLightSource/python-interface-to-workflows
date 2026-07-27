from unittest.mock import MagicMock, patch

from python_interface_to_workflows.submit_to_graphql import submit_workflow_to_graphql


@patch("python_interface_to_workflows.submit_to_argo.os.environ.get")
@patch("python_interface_to_workflows.submit_to_argo.dotenv.load_dotenv")
@patch("python_interface_to_workflows.submit_to_argo.Workflow")
@patch("python_interface_to_workflows.submit_to_graphql.set_token_env_variable")
@patch("python_interface_to_workflows.submit_to_graphql.Client")
def test_submit_workflow_to_graphql(
    mock_client: MagicMock,
    mock_key: MagicMock,
    mock_workflow: MagicMock,
    mock_load_env: MagicMock,
    mock_os_get: MagicMock,
):

    mock_instance = MagicMock()
    mock_key.return_value = "token"
    mock_client.return_value = mock_instance
    mock_instance.execute.return_value = {"submitWorkflow": {"name": "workflow123"}}
    submit_workflow_to_graphql(mock_workflow)
    mock_load_env.assert_called_once_with(dotenv_path="src/.env", override=True)
    mock_instance.execute.assert_called_once()
    mock_workflow.to_yaml.assert_called_once()
    mock_os_get.assert_called_once_with("NAMESPACE")
