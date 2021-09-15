from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from phsw_site.base.api.serializers import RegistrationSerializer
from rest_framework.authtoken.models import Token


@api_view(['POST',])
def registration_view(request):

    if request.method == 'POST':
        serializer = RegistrationSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            user = serializer.save()
            data['response'] = 'Succesfully registered a new user.'
            data['first_name'] = user.first_name
            data['last_name'] = user.last_name
            data['cpf'] = str(user.cpf)  # get serialize error if not convert to string
            data['email'] = user.email
            data['fk_empresa'] = str(user.fk_empresa)
            data['is_agente_admin'] = user.is_agente_admin
            token = Token.objects.get(user=user).key
            data['token'] = token
        else:
            data = serializer.errors
        return Response(data)
