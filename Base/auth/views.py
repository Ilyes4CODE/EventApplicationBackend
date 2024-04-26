from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
from .serializer import RegisterSerializer,ProfileSerializer
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from Base.models import Profile,Events,Ticket
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from Base.serializer import EventSeriliazer,TicketSerializer
from rest_framework.pagination import PageNumberPagination
from django.contrib.auth.password_validation import validate_password
@api_view(['GET'])
def AuthDocumentation(request):
    Doc = {
        'Key':'value',
    }
    return Response(Doc)


@api_view(['POST'])
def register(request):
    data = request.data
    serilizer = RegisterSerializer(data=data)
    if serilizer.is_valid():
        password = data['password']
        try:
            validate_password(password)
        except ValidationError as e:
            return Response({'msg': e.messages[0]}, status=status.HTTP_400_BAD_REQUEST)
            
        if not User.objects.filter(username =data['email']).exists():
            user = User.objects.create(
            username = data['email'],
            password = make_password(data['password'])
        )
            Profile.objects.create(
            user = user,
            first_name = data['first_name'],
            last_name = data['last_name'],
            email = data['email'],
            phone_number = data['phone_number']
        )
            return Response({'info':'your account created'},status=status.HTTP_201_CREATED)
        else:
            return Response({'info':'Username not found Please create an account'})
    return Response(serilizer.errors)
    
    

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def UserProfile(request):
    profile = Profile.objects.get(user=request.user)
    serializer = ProfileSerializer(profile,many=False)
    return Response(serializer.data,status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def Related_Events(request):
    related_events = Events.objects.filter(related_user=request.user)
    paginator = PageNumberPagination()
    paginator.page_size = 2 
    result_page = paginator.paginate_queryset(related_events, request)
    serializer = EventSeriliazer(result_page, many=True)
    return paginator.get_paginated_response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def Related_Tickets(request):
    related_tickets = Ticket.objects.filter(user=request.user)
    paginator = PageNumberPagination()
    paginator.page_size = 10
    result_page = paginator.paginate_queryset(related_tickets,request)
    serializer = TicketSerializer(result_page,many=True)
    return paginator.get_paginated_response(serializer.data)


