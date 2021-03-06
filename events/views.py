from django.shortcuts import render, get_object_or_404
from django.views import View
from django.db.models import Q
from rest_framework import views
from datetime import date, datetime
from rest_framework.response import Response

from .serializers import *
# Create your views here.

class BlockEventsViewSetAPI(views.APIView):
    def get(self, request):
        serializerEvents = EventBlockSerializer(Event.objects.filter(main = True)[:9], many=True)
        dataEvents = serializerEvents.data
        from image_cropping.utils import get_backend
        for event in dataEvents:
            ID = event.get("id")
            obj = Event.objects.get(id=ID)
            image = get_backend().get_thumbnail_url(
                obj.imageOld,
                {
                    'size': (390, 280),
                    'box': obj.image,
                    'crop': True,
                    'detail': True,
                }
            )
            event['image'] = image
        return Response(dataEvents)

class EventsAllViewSet(views.APIView):
    def get(self, request, page):
        trend = int(request.GET.get("direction","-1"))
        dateStartStr = request.GET.get("from","-")
        dateEndStr = request.GET.get("to", "-")
        offset = int(page)
        if trend == -1:
            if dateEndStr == "-" and dateStartStr == "-":
                serializerEvents = EventBlockSerializer(Event.objects.all().reverse()[offset:offset+12], many=True)
            else:
                dateEnd = datetime.strptime(dateEndStr, '%d.%m.%Y')
                dateStart = datetime.strptime(dateStartStr, '%d.%m.%Y')
                setEvents = Event.objects.filter(Q(dateEnd__range=(dateStart, dateEnd)) | Q(dateStart__range=(dateStart, dateEnd))).reverse()
                serializerEvents = EventBlockSerializer(setEvents[offset:offset+12], many=True)
        elif dateEndStr == "-" and dateStartStr == "-":
            serializerEvents = EventBlockSerializer(Event.objects.filter(directions__id_fk__id=trend).distinct()[offset:offset + 12], many=True)
        else:
            dateEnd = datetime.strptime(dateEndStr, '%d.%m.%Y')
            dateStart = datetime.strptime(dateStartStr, '%d.%m.%Y')
            setEvents = Event.objects.filter(Q(dateEnd__range=(dateStart, dateEnd)) | Q(dateStart__range=(dateStart, dateEnd))).filter(directions__id_fk__id=trend).distinct()
            serializerEvents = EventBlockSerializer(setEvents[offset:offset + 12], many=True)
        return Response(getDataEvents(serializerEvents))

class EventsActiveViewSet(views.APIView):
    def get(self, request, page):
        trend = int(request.GET.get("direction","-1"))
        dateStartStr = request.GET.get("from","-")
        dateEndStr = request.GET.get("to", "-")
        offset = int(page)
        if trend == -1:
            if dateEndStr == "-" and dateStartStr == "-":
                serializerEvents = EventBlockSerializer(Event.objects.filter(dateEnd__gte = date.today())[offset:offset+12], many=True)
            else:
                dateEnd = datetime.strptime(dateEndStr, '%d.%m.%Y')
                dateStart = datetime.strptime(dateStartStr, '%d.%m.%Y')
                setEvents = Event.objects.filter(dateEnd__gte = date.today()).filter(Q(dateEnd__range=(dateStart, dateEnd)) | Q(dateStart__range=(dateStart, dateEnd))).reverse()
                serializerEvents = EventBlockSerializer(setEvents[offset:offset+12], many=True)
        elif dateEndStr == "-" and dateStartStr == "-":
            serializerEvents = EventBlockSerializer(Event.objects.filter(directions__id_fk__id=trend, dateEnd__gte = date.today()).distinct()[offset:offset + 12], many=True)
        else:
            dateEnd = datetime.strptime(dateEndStr, '%d.%m.%Y')
            dateStart = datetime.strptime(dateStartStr, '%d.%m.%Y')
            setEvents = Event.objects.filter(dateEnd__gte = date.today()).filter(Q(dateEnd__range=(dateStart, dateEnd)) | Q(dateStart__range=(dateStart, dateEnd))).filter(directions__id_fk__id=trend).distinct()
            serializerEvents = EventBlockSerializer(setEvents[offset:offset + 12], many=True)
        return Response(getDataEvents(serializerEvents))

class EventsCompletedViewSet(views.APIView):
    def get(self, request, page):
        trend = int(request.GET.get("direction","-1"))
        dateStartStr = request.GET.get("from","-")
        dateEndStr = request.GET.get("to", "-")
        offset = int(page)
        if trend == -1:
            if dateEndStr == "-" and dateStartStr == "-":
                serializerEvents = EventBlockSerializer(Event.objects.filter(dateEnd__lt = date.today())[offset:offset+12], many=True)
            else:
                dateEnd = datetime.strptime(dateEndStr, '%d.%m.%Y')
                dateStart = datetime.strptime(dateStartStr, '%d.%m.%Y')
                setEvents = Event.objects.filter(dateEnd__lt = date.today()).filter(Q(dateEnd__range=(dateStart, dateEnd)) | Q(dateStart__range=(dateStart, dateEnd))).reverse()
                serializerEvents = EventBlockSerializer(setEvents[offset:offset+12], many=True)
        elif dateEndStr == "-" and dateStartStr == "-":
            serializerEvents = EventBlockSerializer(Event.objects.filter(directions__id_fk__id=trend, dateEnd__lt = date.today()).distinct()[offset:offset + 12], many=True)
        else:
            dateEnd = datetime.strptime(dateEndStr, '%d.%m.%Y')
            dateStart = datetime.strptime(dateStartStr, '%d.%m.%Y')
            setEvents = Event.objects.filter(dateEnd__lt = date.today()).filter(Q(dateEnd__range=(dateStart, dateEnd)) | Q(dateStart__range=(dateStart, dateEnd))).filter(directions__id_fk__id=trend).distinct()
            serializerEvents = EventBlockSerializer(setEvents[offset:offset + 12], many=True)
        return Response(getDataEvents(serializerEvents))

def getDataEvents(serializerEvents):
    dataEvents = serializerEvents.data
    from image_cropping.utils import get_backend
    for opp in dataEvents:
        ID = opp.get("id")
        obj = Event.objects.get(id=ID)
        image = get_backend().get_thumbnail_url(
            obj.imageOld,
            {
                'size': (390, 280),
                'box': obj.image,
                'crop': True,
                'detail': True,
            }
        )
        opp['image'] = image
    return dataEvents

class EventDetail(views.APIView):
    def get(self, request, pk):
        id = int(pk)
        event = get_object_or_404(Event, id=id)

        similar_event = list()
        counterSimilarEvent = 0
        listUniqueTrends = list()

        for direction in event.directions.all():
            listUniqueTrends.append(direction.id_fk)
        listUniqueTrends = list(set(listUniqueTrends))
        for trend in listUniqueTrends:
            for direction in Direction.objects.filter(id_fk = trend):
                for obj in direction.event_set.all():
                    if obj.id is not event.id:
                        similar_event.append(obj)
                        counterSimilarEvent += 1
                    if counterSimilarEvent == 3:
                        break
                if counterSimilarEvent == 3:
                    break
            if counterSimilarEvent == 3:
                break
        similar_event = list(set(similar_event))


        from image_cropping.utils import get_backend
        image = get_backend().get_thumbnail_url(
            event.imageOld,
            {
                'size': (900, 315),
                'box': event.imageBig,
                'crop': True,
                'detail': True,
            }
        )
        serializerEvent = EventSerializer(event)
        eventData = serializerEvent.data
        eventData['image'] = image

        serializerSimilarEvent = EventNextPrevSimilarSerializer(similar_event, many=True)


        return Response({
            "event": eventData,
            "similarEvents": serializerSimilarEvent.data,
       })