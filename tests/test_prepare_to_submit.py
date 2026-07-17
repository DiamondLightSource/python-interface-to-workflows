from unittest.mock import MagicMock, call, patch

from python_interface_to_workflows.prepare_to_submit import prepare_to_submit


@patch("python_interface_to_workflows.prepare_to_submit.os.environ.get")
@patch("python_interface_to_workflows.prepare_to_submit.dotenv.load_dotenv")
@patch("python_interface_to_workflows.prepare_to_submit.set_token_env_variable")
def test_prep_submit_a_workflow(
    mock_key: MagicMock, mock_load_env: MagicMock, mock_get_env_var: MagicMock
):

    prepare_to_submit(True)
    mock_key.assert_called_once_with(staging=True)
    mock_load_env.assert_called_once_with(dotenv_path="src/.env", override=True)
    mock_get_env_var.assert_has_calls(
        [call("HOST"), call("IMAGE"), call("TOKEN")], any_order=True
    )
