from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError

from rest_framework.pagination import PageNumberPagination

from .models import User
from .serializer import CreateUserSerializer




@api_view(["POST", "GET"])
def users_view(request):

    """Realizado con IA"""
    if request.method == "POST":
        serializer = CreateUserSerializer(data=request.data)

        if serializer.is_valid():
            try:
                user = serializer.save()
                return Response(
                    {
                        "id": user.id,
                        "email": user.email,
                        "first_name": user.first_name,
                        "last_name": user.last_name,
                    },
                    status=status.HTTP_201_CREATED,
                )
            except ValidationError as e:
                return Response(
                    {
                        "error": {
                            "code": "EMAIL_ALREADY_EXISTS",
                            "message": str(e),
                        }
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

        return Response(
            {
                "error": {
                    "code": "INVALID_DATA",
                    "message": "Invalid input",
                    "details": serializer.errors,
                }
            },
            status=status.HTTP_400_BAD_REQUEST,
        )




    if request.method == "GET":
        users = User.objects.all().order_by("-date_joined")
        
        paginator = PageNumberPagination()
        paginator.page_size = 10
        resultado = paginator.paginate_queryset(users, request)

        data = [
            {
                "id": user.id,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
            }
            for user in resultado
        ]

        return Response(data, status=status.HTTP_200_OK)
    