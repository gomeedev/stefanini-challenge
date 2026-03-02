from groq import Groq
from django.conf import settings

from user.models import User
from tasks.models import StatusChoice, Task




# Servicio para manejar consultas con Groq
class AssistantService:
    
    def __init__(self):
        self.client = Groq(api_key=settings.GROQ_API_KEY)
        self.model = "llama-3.3-70b-versatile"
        
        
    def get_context(self):
        total_users = User.objects.count()
        total_task = Task.objects.count()
        
        context = "Contexto de la aplicación de tareas con colaboración"
        
        context += f"Total de usuarios: {total_users}"
        context += f"Total de tareas: {total_task}"
        
        return context
        
    
    def consult(self, user_question):
        data_context = self.get_context()
        
        prompt_system = """Eres **Alex**, un asistente y Análista inteligente que facilita la gestión de tareas para los usuarios, tu misión es permitirles gestionar mejor su flujo de trabajo con guias y enseñanzas practicas.
        
        REGLAS IMPORTANTES:
        1. Solo puedes responder con preguntas basadas en el contexto proporcionado, evitar dar información falsa y/o alucinar.
        2. Si no tienes la información o no puedes responder una pregunta, se honesto y aclara que no tienes información suficiente para esa pregunta.
        3. Nos gusta la argumentación y la ciencia. Por ende, trata de explicar todo con profundidad y la razón de tus decisiones.
        4. Saluda al equipo (Harold, Jessica, Sara, jennifer y Saira) al final del texto (hazlo con poco margén por respuesta, para evitar que todos los ouputs muestren el saludo). 
        
        
        Contexto actual del sistema: \n\n:
        """
        
        prompt_system += data_context
        
        mesagges = [
            {
                "role": "system", 
                "content": prompt_system
            }
        ]
        
        mesagges.append({
            "role": "user",
            "content": user_question
        })
        
        try:
            chat_completion = self.client.chat.completions.create(
                messages=mesagges,
                model=self.model,
                temperature=0.4,
                max_tokens=1000
            )
            
            response = chat_completion.choices[0].message.content
            
            mesagges.append({
                "role": "assistant",
                "content": response
            })
            
            return {
                "success": True,
                "respuesta": response
            }
        except Exception as e:
            return {
                "succes": False,
                "error": f"Error al consultarle a groq: {str(e)}"
            }
