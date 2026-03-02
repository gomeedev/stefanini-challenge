from groq import Groq
from django.conf import settings

from user.models import User
from tasks.models import Task


_historial_store = {}


# Servicio para manejar consultas con Groq
class AssistantService:
    
    def __init__(self):
        self.client = Groq(api_key=settings.GROQ_API_KEY)
        self.model = "llama-3.3-70b-versatile"
        
        
    def get_context(self, user_id=None):
        
        context = "CONTEXTO DEL SISTEMA: \n"
        
        if user_id:
            try:
                user = User.objects.prefetch_related('tasks').get(id=user_id)
                context += f"usuario actual:\n"
                context += f"- Nombre: {user.first_name} {user.last_name}\n"
                context += f"- Correo: {user.email}\n"

                tasks = user.tasks.all()
                context += f"Tareas asignadas: ({tasks.count()}):\n"
                for task in tasks:
                    context += f"  · [{task.status}] {task.title}\n"
                    if task.description:
                        context += f"    Descripción: {task.description}\n"

            except User.DoesNotExist:
                context += "El usuario con ese id no existe.\n"
                
    
        context += "Resumen general: "    
        context += f"Totao de usuarios {User.objects.count()}"
        context += f"Total de tareas {Task.objects.count()}"
        
        return context
        
    
    def consult(self, session_id, user_question, user_id=None):
        
        history = _historial_store.get(session_id, [])
        
        
        data_context = self.get_context(user_id=user_id)
        prompt_system = f"""Eres **Alex**, un asistente y Análista inteligente que facilita la gestión de tareas para los usuarios, tu misión es permitirles gestionar mejor su flujo de trabajo con guias y enseñanzas practicas.
        
        REGLAS IMPORTANTES:
        1. Solo puedes responder con preguntas basadas en el contexto proporcionado, evitar dar información falsa y/o alucinar.
        2. Si no tienes la información o no puedes responder una pregunta, se honesto y aclara que no tienes información suficiente para esa pregunta.
        3. Nos gusta la argumentación y la ciencia. Por ende, trata de explicar todo con profundidad y la razón de tus decisiones.
        4. Ocasionalmente, dinos un dato curioso sobre la computación y áreas afines a esta, datos muy profundos que nos incentiven a pensar y/o reflexionar. 
        
        
        Contexto actual del sistema: \n\n:
        {data_context}
        """
        
        mesagges = [
            {
                "role": "system", 
                "content": prompt_system
            }
        ]
        
        mesagges.extend(history)
        
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
            
            history.append({
                "role": "user",
                "content": user_question
            })
            
            history.append({
                "role": "assistant",
                "content": response
            })
            
            _historial_store[session_id] = history
            
            return {
                "success": True,
                "respuesta": response,
            }
            
        except Exception as e:
            return {
                "succes": False,
                "error": f"Error al consultarle a groq: {str(e)}"
            }
