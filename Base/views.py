from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated
from .serializer import CreateEventSerializer,EventSeriliazer
from django.shortcuts import get_object_or_404
from .models import Events,Ticket,Profile
from rest_framework import status
@api_view(['GET'])
def SystemDocumentation(request):
    Doc = {
        'Key':'value',
    }
    return Response(Doc)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def PostEvent(request):
    data = request.data
    serializer = CreateEventSerializer(data=data, request=request)
    if serializer.is_valid():
        serializer.save() 
        return Response(serializer.data, status=201) 
    return Response(serializer.errors, status=400) 

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def Enroll_in_Event(request,pk):
    the_event = get_object_or_404(Events,pk=pk)
    if the_event.enrollment_limit == 0:
        return Response({'info':'there is no places left'},status=status.HTTP_502_BAD_GATEWAY)
    if request.user not in the_event.enrolled_users.all():
        the_event.enrolled_users.add(request.user)
        the_event.enrollment_limit -= 1
        the_event.save()
        Ticket.objects.create(
            user = request.user,
            event = the_event,
        )
        return Response({'info':'you have been enrolled'},status=status.HTTP_200_OK)
    else:
        return Response({'info':'you already enrolled'},status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def Like_Event(request,pk):
    event = get_object_or_404(Events,pk=pk)
    if request.user in event.likers.all():
        event.likers.remove(request.user)
        return Response({'info':'like removed'})
    elif request.user in event.dislikers.all():
        event.dislikers.remove(request.user)
        event.likers.add(request.user)
        return Response({'info':'like added'})
    elif request.user not in event.likers.all():
        event.likers.add(request.user)
        return Response({'info':'like added'})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def Dislike_Event(request, pk):
    event = get_object_or_404(Events, pk=pk)

    if request.user in event.dislikers.all():
        event.dislikers.remove(request.user)
        return Response({'info': 'dislike removed'})
    elif request.user in event.likers.all():
        event.likers.remove(request.user)
        event.dislikers.add(request.user)
        return Response({'info': 'dislike added'})
    else:
        event.dislikers.add(request.user)
        return Response({'info': 'dislike added'})
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def Follow_Profile(request,pk):
    profile = get_object_or_404(Profile,pk=pk)
    if request.user == profile.user:
        return Response({'info':'you cannot follow yourself'})
    elif request.user not in profile.followers.all():
        profile.followers.add(request.user)
        return Response({'info':'follow succefully'})
    else: 
        profile.followers.remove(request.user)
        return Response({'info':'follow removed'})

@api_view(['GET'])
def search_events_by_title(request):
    title = request.query_params.get('title', None)
    if title is None:
        return Response({'error': 'Title parameter is missing'}, status=400)

    try:
        events = Events.objects.filter(title__icontains=title)
        serializer = EventSeriliazer(events, many=True)
        return Response(serializer.data, status=200)
    except Events.DoesNotExist:
        return Response({'error': 'No events found matching the search query'}, status=404)