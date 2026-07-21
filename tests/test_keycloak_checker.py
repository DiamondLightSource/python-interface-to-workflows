import os
from unittest.mock import MagicMock, patch

from pytest import mark

from python_interface_to_workflows.auth.keycloak_checker import set_token_env_variable


@mark.parametrize("dev,port", [(True, 5173), (False, 8000)])
@patch("python_interface_to_workflows.auth.keycloak_checker.KeycloakOpenID")
@patch("python_interface_to_workflows.auth.keycloak_checker.generate_code_verifier")
@patch("python_interface_to_workflows.auth.keycloak_checker.generate_code_challenge")
@patch("python_interface_to_workflows.auth.keycloak_checker.open_auth_url")
def test_return_key(
    mock_open_auth_url: MagicMock,
    mock_gen_code_challenge: MagicMock,
    mock_gen_code_verifier: MagicMock,
    mock_gen_keycloak_id: MagicMock,
    dev: bool,
    port: int,
):
    mock_gen_code_verifier.return_value = "verifier"
    mock_gen_code_challenge.return_value = ("challenge", "S256")
    os.environ["AUTH"] = "auth_url_code"
    keycloak = MagicMock()
    mock_gen_keycloak_id.return_value = keycloak

    keycloak.auth_url.return_value = "https://mock.site"
    keycloak.token.return_value = {
        "access_token": "fake_token",
        "refresh_token": "fake_refresh",
    }
    assert set_token_env_variable(dev) == "fake_token"
    mock_open_auth_url.assert_called_once_with("https://mock.site", port)
    keycloak.token.assert_called_once_with(
        grant_type="authorization_code",
        code="auth_url_code",
        redirect_uri=f"http://localhost:{port}/",
        code_verifier="verifier",
    )
