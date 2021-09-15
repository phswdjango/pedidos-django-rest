from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from phsw_site.base.api.serializers import RegistrationSerializer, UserSerializer
from rest_framework.authtoken.models import Token
from phsw_site.base.models import User


@api_view(['POST', ])
@permission_classes([IsAuthenticated])
def registration_view(request):
    if request.user.all_api_permissions:
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
    return Response({'response': 'Nao possui permissoes para acessar esse recurso.'},
                    status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET', ])
@permission_classes([IsAuthenticated])
def check_user_view(request, slug):
    if request.user.all_api_permissions:
        try:
            user = User.objects.get(id=slug)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = UserSerializer(user)
        return Response(serializer.data)
    return Response({'response': 'Nao possui permissoes para acessar esse recurso.'},
                    status=status.HTTP_401_UNAUTHORIZED)