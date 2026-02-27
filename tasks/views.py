from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError

from .models import Task
from .serializer import (TaskSerializer, CreateTaskSerializer, UpdateStatusSerializer, AssignTaskSerializer,)
from .services import list_tasks




@api_view(["GET", "POST"])
def tasks_view(request):

    if request.method == "GET":
        status_filter = request.query_params.get('status')
        name_filter = request.query_params.get('assigned_name')

        tasks = list_tasks(status=status_filter, assigned_name=name_filter)
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    if request.method == "POST":
        serializer = CreateTaskSerializer(data=request.data)
        if serializer.is_valid():
            try:
                task = serializer.save()
                return Response(TaskSerializer(task).data, status=status.HTTP_201_CREATED)
            except ValidationError as e:
                return Response(
                    {"error": 
                        {
                            "code": "INVALID_DATA", 
                            "message": e.detail
                        }
                    }, status=status.HTTP_400_BAD_REQUEST
                )

        return Response(
            {"error": 
                {
                    "code": "INVALID_DATA", 
                    "message": serializer.errors
                }
            }, status=status.HTTP_400_BAD_REQUEST
        )


"""Hecho con IA"""
@api_view(["PATCH"])
def task_status_view(request, pk):
    try:
        task = Task.objects.get(id=pk)
    except Task.DoesNotExist:
        return Response(
            {"error": 
                {
                    "code": "NOT_FOUND", 
                    "message": "Tarea no encontrada"}
            }, status=status.HTTP_404_NOT_FOUND
        )

    serializer = UpdateStatusSerializer(data=request.data)
    if serializer.is_valid():
        try:
            task = serializer.update(task, serializer.validated_data)
            return Response(TaskSerializer(task).data, status=status.HTTP_200_OK)
        except ValidationError as e:
            return Response(
                {"error": 
                    {
                        "code": "INVALID_TRANSITION", 
                        "message": e.detail
                    }
                }, status=status.HTTP_400_BAD_REQUEST
            )

    return Response(
        {"error": 
            {
                "code": "INVALID_DATA", 
                "message": serializer.errors
            }
        }, status=status.HTTP_400_BAD_REQUEST
    )


"""Hecho con IA"""
@api_view(["PATCH"])
def task_assign_view(request, pk):
    try:
        task = Task.objects.get(id=pk)
    except Task.DoesNotExist:
        return Response(
            {"error": 
                {
                    "code": "NOT_FOUND", 
                    "message": "Tarea no encontrada"
                }
            }, status=status.HTTP_404_NOT_FOUND)

    serializer = AssignTaskSerializer(data=request.data)
    if serializer.is_valid():
        try:
            task = serializer.update(task, serializer.validated_data)
            return Response(TaskSerializer(task).data, status=status.HTTP_200_OK)
        except ValidationError as e:
            return Response(
                {"error": 
                    {
                        "code": "INVALID_DATA", 
                        "message": e.detail
                    }
                }, status=status.HTTP_400_BAD_REQUEST)

    return Response(
        {"error": 
            {
                "code": "INVALID_DATA", 
                "message": serializer.errors
            }
        }, status=status.HTTP_400_BAD_REQUEST)
