from unittest.mock import AsyncMock, MagicMock, call, patch

import pytest

from python_interface_to_workflows.submit_workflow import submit_workflow


@pytest.mark.asyncio
@patch("python_interface_to_workflows.submit_workflow.os.environ.get")
@patch("python_interface_to_workflows.submit_workflow.dotenv.load_dotenv")
@patch("python_interface_to_workflows.submit_workflow.Workflow")
@patch("python_interface_to_workflows.submit_workflow.set_token_env_variable")
@patch("python_interface_to_workflows.submit_workflow.Client")
async def test_submit_workflow_to_graphql(
    mock_client: AsyncMock,
    mock_key: MagicMock,
    mock_workflow: MagicMock,
    mock_load_env: MagicMock,
    mock_os_get: MagicMock,
):

    mock_instance = AsyncMock()
    mock_key.return_value = "token"
    mock_client.return_value = mock_instance
    mock_instance.execute_async = AsyncMock(
        return_value={"submitWorkflow": {"name": "workflow123"}}
    )
    await submit_workflow(mock_workflow)
    mock_load_env.assert_called_once_with(dotenv_path="src/.env", override=True)
    mock_instance.execute_async.assert_called_once()
    mock_workflow.to_yaml.assert_called_once()
    mock_os_get.assert_has_calls([call("VISIT"), call("HOST")], any_order=True)
