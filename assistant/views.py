from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from drf_spectacular.utils import extend_schema, OpenApiParameter

from .services import AssistantService





@extend_schema(
    tags=["Alex"],
    summary="Consultar al asistente",
    description="Este endpoint es para interactuar con el asistente de IA, mantiene historial por session_id.",
    request={
        "application/json": {
            "type": "object",
            "properties": {
                "pregunta":   {"type": "string", "example": "¿Quién soy?"},
                "session_id": {"type": "string", "example": "sesion-1"},
                "user_id":    {"type": "integer", "example": 2},
            },
            "required": ["pregunta", "session_id"]
        }
    },
    responses={
        200: {
            "type": "object",
            "properties": {
                "pregunta":  {"type": "string"},
                "respuesta": {"type": "string"},
            }
        }
    }
)
@api_view(['POST'])
def consult_assistan(request):
    
    question = request.data.get('pregunta')
    user_id  = request.data.get('user_id') 
    session_id = request.data.get('session_id') 
    
    if not question:
        return Response(
            {
                "error": "Debes enviar una 'pregunta' en el body",
            }, status=status.HTTP_400_BAD_REQUEST
        )
    
    if not session_id:
        return Response(
            {"error": "Debes enviar un session_id"},
            status=status.HTTP_400_BAD_REQUEST
        )

    
    service = AssistantService()
    result = service.consult(session_id, question, user_id=user_id)
    
    if result['success']:
        return Response({
            "pregunta": question,
            "respuesta": result['respuesta'],
        }, status=status.HTTP_200_OK)
    else:
        return Response(
            {
                "error": result['error']
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
