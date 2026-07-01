import os

from keycloak import KeycloakOpenID

# from keycloak.exceptions import KeycloakPostError
from keycloak.pkce_utils import generate_code_challenge, generate_code_verifier

from python_interface_to_workflows.auth.open_auth_url import open_auth_url


def return_key(dev: bool) -> str:
    match dev:
        case True:
            keycloak_openid = KeycloakOpenID(
                server_url="https://identity.diamond.ac.uk/",
                client_id="workflows-ui-dev",
                realm_name="dls",
                client_secret_key="",
                pool_maxsize=1,
            )
        case False:
            keycloak_openid = KeycloakOpenID(
                client_id="workflows-dashboard",
                server_url="https://identity.diamond.ac.uk/",
                realm_name="dls",
                client_secret_key="",
                pool_maxsize=1,
            )
    # btw, as you review this, I don't think this try-except is
    # necessary - pretty certain this functionality is already in keycloak
    # as the tokens i've seen are suspiciously similar and also don't require a login
    # which i believe is due to it figuring out we already have a refresh token
    # ergo, not confident that this hashed out stuff is needed.
    # try:
    #     newtoken: dict[str, str] = (  # pyright: ignore[reportUnknownVariableType]
    #         keycloak_openid.refresh_token(  # pyright: ignore[reportUnknownMemberType]
    #             os.environ.get("REFRESH")  # pyright: ignore[reportArgumentType]
    #         )
    #     )
    #     return newtoken["access_token"]
    # except KeycloakPostError:
    code_verifier = generate_code_verifier()
    code_challenge, code_challenge_method = generate_code_challenge(code_verifier)
    auth_url = keycloak_openid.auth_url(
        redirect_uri="http://localhost:5173/",
        scope="openid posix-uid profile email fedid",
        state="",
        code_challenge=code_challenge,
        code_challenge_method=code_challenge_method,
    )
    open_auth_url(auth_url)
    token: dict[str, str] = (  # pyright: ignore[reportUnknownVariableType]
        keycloak_openid.token(  # pyright: ignore[reportUnknownMemberType]
            grant_type="authorization_code",
            code=os.environ["AUTH"],
            redirect_uri="http://localhost:5173/",
            code_verifier=code_verifier,
        )
    )
    os.environ["REFRESH"] = token["refresh_token"]
    os.environ["TOKEN"] = token["access_token"]
    return token["access_token"]  # pyright: ignore[reportUnknownArgumentType]
