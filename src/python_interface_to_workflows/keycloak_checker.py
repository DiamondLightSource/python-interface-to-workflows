import urllib.parse
import webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import cast

from keycloak import KeycloakOpenID

# Configure client
# For versions older than 18 /auth/ must be added at the end of the server_url.
from keycloak.pkce_utils import generate_code_challenge, generate_code_verifier


def _open_auth_url(auth_url: str) -> str:
    webbrowser.open(auth_url)

    class _ReusingHTTPServer(HTTPServer):
        allow_reuse_address = True
        auth_code: str

    class CallbackHandler(BaseHTTPRequestHandler):
        def do_GET(self):
            query = urllib.parse.urlparse(self.path).query
            params = urllib.parse.parse_qs(query)
            if "code" in params:
                cast(_ReusingHTTPServer, self.server).auth_code = params["code"][0]
                self.send_response(200)
                self.end_headers()
                self.wfile.write(
                    b"Authorization successful. You can close this window."
                )
            else:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b"Missing authorization code.")

    httpd = _ReusingHTTPServer(("localhost", 5173), CallbackHandler)
    httpd.handle_request()  # Wait for one request
    auth_code = httpd.auth_code
    httpd.server_close()
    return auth_code


def return_key(dev: bool) -> str:
    match dev:
        case True:
            keycloak_openid = KeycloakOpenID(
                server_url="https://identity-test.diamond.ac.uk/",
                client_id="workflows-ui-dev",
                realm_name="dls",
                client_secret_key="",
                pool_maxsize=1,
            )
        case False:
            keycloak_openid = KeycloakOpenID(
                client_id="workflows-dashboard",
                server_url="https://identity-test.diamond.ac.uk/",
                realm_name="dls",
                client_secret_key="",
                pool_maxsize=1,
            )

    code_verifier = generate_code_verifier()
    code_challenge, code_challenge_method = generate_code_challenge(code_verifier)
    auth_url = keycloak_openid.auth_url(
        redirect_uri="http://localhost:5173/",
        scope="openid posix-uid profile email fedid",
        state="",
        code_challenge=code_challenge,
        code_challenge_method=code_challenge_method,
    )

    auth_code = _open_auth_url(auth_url)

    access_token: dict[str, str] = keycloak_openid.token(  # pyright: ignore[reportUnknownMemberType]
        grant_type="authorization_code",
        code=auth_code,
        redirect_uri="http://localhost:5173/",
        code_verifier=code_verifier,
        code_challenge=code_challenge,
    )
    return str(access_token["access_token"])  # pyright: ignore[reportUnknownArgumentType]


# refresh token lasts 15 mins over the normal token which lasts 15 mins itself
