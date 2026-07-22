from unittest.mock import MagicMock, call, patch

from python_interface_to_workflows.submit_to_argo import submit_workflow_to_argo


@patch("python_interface_to_workflows.submit_to_argo.Workflow")
@patch("python_interface_to_workflows.submit_to_argo.os.environ.get")
@patch("python_interface_to_workflows.submit_to_argo.dotenv.load_dotenv")
@patch("python_interface_to_workflows.submit_to_argo.set_token_env_variable")
def test_submit_workflow_to_argo(
    mock_key: MagicMock,
    mock_load_env: MagicMock,
    mock_get_env_var: MagicMock,
    mock_workflow: MagicMock,
):
    mock_workflow = MagicMock()
    submit_workflow_to_argo(mock_workflow)
    mock_key.assert_called_once_with(staging=True)
    mock_load_env.assert_called_once_with(dotenv_path="src/.env", override=True)
    mock_get_env_var.assert_has_calls([call("HOST"), call("TOKEN")], any_order=True)
