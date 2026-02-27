from rest_framework.exceptions import ValidationError
from .models import User



# Harold, no validé formato de correo porque django internamente ya lo hace
def create_user(email:str, first_name:str, last_name:str):
    if User.objects.filter(email=email).exists():
        raise ValidationError({"email": "Este correo ya existe, ingresa uno diferente"})
    
    return User.objects.create(
        # Igualé 'username' con email porque django me obliga y porque no implementaré login
        username=email,
        email=email,
        first_name=first_name,
        last_name=last_name
    )
