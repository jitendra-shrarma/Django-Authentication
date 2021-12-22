# Import RefreshToken, Response and status
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from django.dispatch import receiver
from django.urls import reverse
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import send_mail, EmailMultiAlternatives

# Set refresh_token in COOKIES
def set_refresh_token(response, refresh_token=None):
    if refresh_token:
        response.set_cookie(
            "refresh_token", refresh_token, httponly=True, max_age=(24 * 3600)
        )


# Get refresh_token_str from COOKIES
def get_refresh_token(request):
    refresh_token_str = request.COOKIES.get("refresh_token", None)
    if refresh_token_str is not None:
        return refresh_token_str
    return None


# Set access_token in COOKIES
def set_access_token(response, refresh_token=None):
    if refresh_token:
        response.set_cookie(
            "access_token", refresh_token.access_token, httponly=True, max_age=300
        )


# Get access_token_str from COOKIES
def get_access_token(request):
    access_token_str = request.COOKIES.get("access_token", None)
    if access_token_str is not None:
        return access_token_str
    return None


# Set access_token and refresh_token in COOKIES
def set_cookies(response, refresh_token=None):
    set_access_token(response, refresh_token)
    set_refresh_token(response, refresh_token)


# Remove access_token and refresh_token from COOKIES
def unset_cookies(response):
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")


# Check request for access_token
def get_access_token_response(request=None):
    # If it's a request
    if request:
        access_token = get_access_token(request)
        # And if Request have access_token,
        if access_token:
            # Create "Invalid request" response and return
            response = Response(
                {"message": "Invalid request."}, status=status.HTTP_400_BAD_REQUEST
            )
            return response

        # If request have no access_token, check for refresh token
        refresh_token = get_refresh_token(request)
        # If Request have refresh token,
        if refresh_token:
            # Create "Invalid request" response and create a new access_token
            response = Response(
                {"message": "Invalid request."}, status=status.HTTP_400_BAD_REQUEST
            )
            set_access_token(response, RefreshToken(refresh_token))
            return response

    # If no request is made, return no response
    return None


@receiver(reset_password_token_created)
def password_reset_token_created(
    sender, instance, reset_password_token, *args, **kwargs
):
    """
    Handles password reset tokens
    When a token is created, an e-mail needs to be sent to the user
    :param sender: View Class that sent the signal
    :param instance: View Instance that sent the signal
    :param reset_password_token: Token Model Object
    :param args:
    :param kwargs:
    :return:
    """
    # send an e-mail to the user
    context = {
        "current_user": reset_password_token.user,
        "username": reset_password_token.user.username,
        "email": reset_password_token.user.email,
        "reset_password_url": "{}?token={}".format(
            reverse("password_reset:reset-password-request"), reset_password_token.key
        ),
    }

    # render email text
    # this functionality needs to be implemented,
    # for now user copy token and add new password, make new request on {reverse('password_reset:reset-password-request')}confirm/
    email_plaintext_message = f"{reverse('password_reset:reset-password-request')}?token={reset_password_token.key}"

    msg = EmailMultiAlternatives(
        # title:
        "Password Reset for {title}".format(title="Some website title"),
        # message:
        email_plaintext_message,
        # from:
        "noreply@somehost.local",
        # to:
        [reset_password_token.user.email],
    )
    msg.send()
