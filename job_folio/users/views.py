from django.contrib.auth import get_user_model
from rest_framework import serializers, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from job_folio.users.selectors import users_get_user
from job_folio.users.services import users_update_user

User = get_user_model()


class UserDetailView(APIView):
    permission_classes = [IsAuthenticated]

    class UserDetailOutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = User
            fields = ["id", "email", "first_name", "last_name", "date_joined"]

    def get_serializer_class(self):
        return self.UserDetailOutputSerializer

    def get(self, request, user_id: int):
        user = users_get_user(user_id=user_id)
        serializer = self.UserDetailOutputSerializer(user, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    class UserUpdateInputSerializer(serializers.Serializer):
        first_name = serializers.CharField()
        last_name = serializers.CharField()

    class UserUpdateOutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = User
            fields = ["id", "email", "first_name", "last_name", "date_joined"]

    def get_serializer_class(self):
        return self.UserUpdateOutputSerializer

    def post(self, request):
        serializer = self.UserUpdateInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        prefs = users_update_user(user=request.user, data=serializer.validated_data)
        serializer = self.UserUpdateOutputSerializer(data=prefs)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
