from drf_spectacular.utils import extend_schema
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.users.models import User
from common.exceptions import BadRequest
from common.serializers import ErrorResponse
from .serializers import MyProfileResponse, MyConfigResponse, UpdateMyProfileRequest, UpdateMyProfileResponse, \
    FitbitConfigInfoResponse


@extend_schema(tags=['Users'])
class MyProfileAPIView(APIView):

    @extend_schema(responses={200: MyProfileResponse, 400: ErrorResponse, 500: ErrorResponse})
    def get(self, request):
        user = request.user
        response = MyProfileResponse(user)
        return Response(response.data)

    @extend_schema(request=UpdateMyProfileRequest,
                   responses={200: UpdateMyProfileResponse, 400: ErrorResponse, 500: ErrorResponse})
    def put(self, request):
        serializer = UpdateMyProfileRequest(data=request.data)
        if not serializer.is_valid():
            raise BadRequest(400000, error_detail=serializer.errors)

        user = request.user
        User.objects.filter(id=user.id).update(**serializer.validated_data)
        result = {
            'id': user.id,
            **serializer.validated_data
        }
        response = UpdateMyProfileResponse(result)
        return Response(response.data)


@extend_schema(tags=['Users'])
class MyConfigAPIView(APIView):

    @extend_schema(responses={200: MyConfigResponse, 400: ErrorResponse, 500: ErrorResponse})
    def get(self, request):
        response = FitbitConfigInfoResponse()
        return Response(response.data)
