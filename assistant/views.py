from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .services import AssistantService




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
