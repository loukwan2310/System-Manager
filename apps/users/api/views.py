from django.conf import settings
from drf_spectacular.utils import extend_schema
from rest_framework.views import APIView
from rest_framework.response import Response

from apps.users.models import User
from common.exceptions import BadRequest
from common.pagination import CustomPagination
from common.serializers import ErrorResponse
from common.constants import FITBIT_RESPONSE_TYPE, FITBIT_CHALLENGE_METHOD, FITBIT_SCOPE
from .serializers import MyProfileResponse, MyConfigResponse, UpdateMyProfileRequest, UpdateMyProfileResponse, \
    UserHairStyleListRequest, UserHairStyleListResponse


@extend_schema(tags=['Users'])
class MyProfileAPIView(APIView):

    @extend_schema(responses={200: MyProfileResponse, 400: ErrorResponse, 500: ErrorResponse})
    def get(self, request):
        user = request.user
        fitbit_user = FitbitUser.objects.filter(target_user=user).first()
        user.fitbit_user = fitbit_user
        response = MyProfileResponse(user)
        return Response(response.data)

    @extend_schema(request=UpdateMyProfileRequest,
                   responses={200: UpdateMyProfileResponse, 400: ErrorResponse, 500: ErrorResponse})
    def put(self, request):
        serializer = UpdateMyProfileRequest(data=request.data)
        if not serializer.is_valid():
            raise BadRequest(400000, error_detail=serializer.errors)

        user = request.user
        hair_style_id = serializer.validated_data.get('hair_style_id')
        if not HairStyle.objects.filter(id=hair_style_id).exists():
            raise BadRequest(400016)
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
        fitbit_config = {
            'client_id': settings.FITBIT_CLIENT_ID,
            'code_challenge': settings.FITBIT_CODE_CHALLENGE,
            'response_type': FITBIT_RESPONSE_TYPE,
            'code_challenge_method': FITBIT_CHALLENGE_METHOD,
            'scope': FITBIT_SCOPE
        }
        response = MyConfigResponse({
            'fitbit': fitbit_config
        })
        return Response(response.data)


@extend_schema(tags=['Users'])
class UserHairStyleListAPIView(APIView, CustomPagination):
    permission_classes = []
    authentication_classes = []

    @extend_schema(parameters=[UserHairStyleListRequest],
                   responses={200: UserHairStyleListResponse, 400: ErrorResponse, 500: ErrorResponse})
    def get(self, request):
        queryset = HairStyle.objects.all().order_by('id')
        count = queryset.count()
        hairstyles = self.paginate_queryset(queryset, request, view=self)
        response = UserHairStyleListResponse({
            'count': count,
            "data": hairstyles
        })
        return Response(response.data)
