def set_cookies(response, refresh_token=None):
    if refresh_token is not None:
        response.set_cookie("access_token", refresh_token.access_token, httponly=True, max_age=300)
        response.set_cookie("refresh_token", refresh_token, httponly=True, max_age=(24 * 3600))

def unset_cookies(response):
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")
