from rest_framework.decorators import api_view
from rest_framework.response import Response
from base.models import Room, Message
from .serializers import RoomSerializer

@api_view(['GET'])
def getRoutes(request):
    routes = [
        'GET /api',
        'GET /api/rooms', 
        'GET /api/room/:id'
    ]
    return Response(routes)

@api_view(['GET'])
def getRooms(request):
    rooms = Room.objects.all()
    serializer = RoomSerializer(rooms, many=True)
    rooms_data = serializer.data 
    return Response(rooms_data)

@api_view(['GET'])
def getRoom(request, pk):
    room = Room.objects.get(id=pk)
    serializer = RoomSerializer(room, many=False)
    room_data = serializer.data 
    return Response(room_data)