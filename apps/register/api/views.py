import googleapiclient.discovery
from django.http import HttpResponse
from drf_spectacular.utils import extend_schema
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.views import APIView

from common.oauth2 import GoogleRawLoginFlowService

API_SERVICE_NAME = 'drive'
API_VERSION = 'v3'


@extend_schema(tags=['Google Login'])
class GoogleLoginRedirectApi(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, *args, **kwargs):
        google_login_flow = GoogleRawLoginFlowService()

        authorization_url, state = google_login_flow.get_authorization_url()
        print(state, "0000000")
        request.session["google_oauth2_state"] = state

        return HttpResponse(authorization_url, content_type="text/html; charset=utf-8")


class InputSerializer(serializers.Serializer):
    code = serializers.CharField(required=False)
    error = serializers.CharField(required=False)
    state = serializers.CharField(required=False)


@extend_schema(tags=['Google Login'])
class GoogleLoginApi(APIView):
    authentication_classes = []
    permission_classes = []
    serializer_class = InputSerializer

    def get(self, request, *args, **kwargs):
        # Here we have made the request validations.

        google_login_flow = GoogleRawLoginFlowService()
        code = request.query_params.get("code")
        google_tokens = google_login_flow.get_tokens(code=code)
        # print(google_tokens.id_token)
        # print(google_tokens)
        user_infor = google_login_flow.get_user_info(google_tokens)
        # drive = googleapiclient.discovery.build(
        #     API_SERVICE_NAME, API_VERSION, credentials=credentials)

        # files = drive.files().list().execute()
        id_token_decoded = google_tokens.decode_id_token()
        # print(user_infor)
        user_email = id_token_decoded["email"]

        # user = user_get(email=user_email)

        # if user is None:
        #     return Response(
        #         {"error": f"User with email {user_email} is not found."},
        #         status=status.HTTP_404_NOT_FOUND
        #     )

        # login(request, user)

        result = {
            "id_token_decoded": id_token_decoded,
            # "user_info": user_info,
        }

        return Response(result)


@extend_schema(tags=['Google Login'])
class TestLoginGoogleAPIView(APIView):
    permission_classes = []
    authentication_classes = []

    def get(self, request):
        import google_auth_oauthlib.flow
        from django.conf import settings
        flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
            'client_secret.json',
            scopes=['https://www.googleapis.com/auth/userinfo.email'])

        # Required, indicate where the API server will redirect the user after the user completes
        # the authorization flow. The redirect URI is required. The value must exactly
        # match one of the authorized redirect URIs for the OAuth 2.0 client, which you
        # configured in the API Console. If this value doesn't match an authorized URI,
        # you will get a 'redirect_uri_mismatch' error.
        flow.redirect_uri = "".join([settings.BASE_BACKEND_URL, settings.REDIRECT_URI])

        # Generate URL for request to Google's OAuth 2.0 server.
        # Use kwargs to set optional request parameters.
        authorization_url, state = flow.authorization_url(
            # Recommended, enable offline access so that you can refresh an access token without
            # re-prompting the user for permission. Recommended for web server apps.
            access_type='offline',
            # Optional, enable incremental authorization. Recommended as a best practice.
            include_granted_scopes='true',
            # Optional, if your application knows which user is trying to authenticate, it can use this
            # parameter to provide a hint to the Google Authentication Server.
            # login_hint='hint@example.com',
            # Optional, set prompt to 'consent' will prompt the user for consent
            # prompt='consent'
        )
        # print(flow.credentials)
        print(authorization_url)
        request.session["google_oauth2_state"] = state

        return HttpResponse(authorization_url)
