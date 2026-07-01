import os
from unittest.mock import MagicMock, patch

from python_interface_to_workflows.auth.open_auth_url import (
    CallbackHandler,
    open_auth_url,
)


@patch("python_interface_to_workflows.auth.open_auth_url.webbrowser.open")
@patch("python_interface_to_workflows.auth.open_auth_url._ReusingHTTPServer")
def test_open_auth_url_normal_function(
    mock_http_server: MagicMock,
    mock_open_browser: MagicMock,
):
    server = mock_http_server.return_value
    server.auth_code = "this_is_your_code"
    open_auth_url("url")
    server.handle_request.assert_called_once()
    mock_open_browser.assert_called_once_with("url")
    server.socket.shutdown.assert_called_once()
    server.server_close.assert_called_once()
    assert os.environ["AUTH"] == "this_is_your_code"


@patch("python_interface_to_workflows.auth.open_auth_url.exit")
@patch("python_interface_to_workflows.auth.open_auth_url.webbrowser.open")
@patch("python_interface_to_workflows.auth.open_auth_url._ReusingHTTPServer")
def test_open_auth_url_raises_error(
    mock_http_server: MagicMock,
    mock_open_browser: MagicMock,
    mock_exit: MagicMock,
):
    server = mock_http_server.return_value
    server.auth_code = "this_is_your_code"
    server.handle_request.side_effect = OSError
    open_auth_url("url")
    mock_open_browser.assert_called_once_with("url")
    assert os.environ["AUTH"] == ""
    mock_exit.assert_called_once_with(1)
    server.socket.shutdown.assert_called_once()
    server.server_close.assert_called_once()


def test_handler_normal_function():
    handler = CallbackHandler.__new__(CallbackHandler)
    handler.path = "/?code=this_is_your_code"

    handler.server = MagicMock()

    handler.send_response = MagicMock()
    handler.end_headers = MagicMock()
    handler.wfile = MagicMock()
    handler.wfile.write = MagicMock()

    handler.do_GET()

    assert handler.server.auth_code == "this_is_your_code"
    handler.send_response.assert_called_once_with(200)
    handler.wfile.write.assert_called_once_with(
        b"Authorization successful. You can close this window."
    )


def test_handler_error_response():
    handler = CallbackHandler.__new__(CallbackHandler)
    handler.path = "/"

    handler.server = MagicMock()

    handler.send_response = MagicMock()
    handler.end_headers = MagicMock()
    handler.wfile = MagicMock()
    handler.wfile.write = MagicMock()

    handler.do_GET()

    handler.send_response.assert_called_once_with(400)
    handler.end_headers.assert_called_once()
    handler.wfile.write.assert_called_once_with(b"Missing authorization code.")
