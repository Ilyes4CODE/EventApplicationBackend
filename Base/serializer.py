from rest_framework import serializers
from .models import Events,Ticket

class CreateEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Events
        fields = ['related_user', 'title', 'content', 'image', 'is_paid', 'price', 'enrollment_limit']

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(CreateEventSerializer, self).__init__(*args, **kwargs)

    def validate(self, data):
        if not data.get('is_paid', False):
            data['price'] = 0.0

        data['related_user'] = self.request.user
        return data
    
class EventSeriliazer(serializers.ModelSerializer):
    class Meta:
        model = Events
        fields = '__all__'


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = '__all__'