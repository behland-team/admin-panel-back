from django.contrib.auth import get_user_model
from rest_framework import viewsets, permissions, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from .serializer import UserSerializer, UserCreateSerializer


User = get_user_model()

class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_staff)

class RegisterView(generics.CreateAPIView):
    serializer_class = UserCreateSerializer
    permission_classes = [permissions.AllowAny]

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by("-date_joined")

    def get_serializer_class(self):
        # برای ساخت یوزر جدید، از سریالایزر ساخت استفاده کن که password دارد
        if self.action == "create":
            return UserCreateSerializer
        return UserSerializer

    def get_permissions(self):
        if self.action in ["list", "retrieve", "create", "update", "partial_update", "destroy"]:
            return [IsAdmin()]
        return [permissions.IsAuthenticated()]

    def perform_create(self, serializer):
        # استفاده از منیجر تا set_password و پرچم‌ها درست اعمال بشن
        data = serializer.validated_data
        password = data.pop("password")
        user = User.objects.create_user(password=password, **data)
        self.created_user = user  # اگر خواستی در response ازش استفاده کنی

    def create(self, request, *args, **kwargs):
        # خروجی را با UserSerializer بدهیم (بدون password)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        display_ser = UserSerializer(self.created_user)
        headers = self.get_success_headers(display_ser.data)
        return Response(display_ser.data, status=201, headers=headers)

    def perform_update(self, serializer):
        # اگر ادمین در update/partial_update پسورد فرستاد، set_password کن
        password = self.request.data.get("password")
        user = serializer.save()
        if password:
            user.set_password(password)
            user.save()


    @action(detail=False, methods=["get"], permission_classes=[permissions.IsAuthenticated])
    def me(self, request):
        return Response(UserSerializer(request.user).data)
