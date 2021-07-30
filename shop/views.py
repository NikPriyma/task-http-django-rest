from datetime import datetime

from django.db.models.query import QuerySet
from django.db.models import Q

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView

from .models import City, Street, Shop
from .serializers import CitySerializer, StreetSerializer, ShopSerializer


class CityListView(ListCreateAPIView):
    queryset = City.objects
    serializer_class = CitySerializer

    def handle_exception(self, exc):
        return Response(status=400)


class StreetView(ListCreateAPIView):
    queryset = Street.objects
    serializer_class = StreetSerializer

    def get(self, request, *args, **kwargs):
        city_id = str(
            kwargs.get('city_id', request.query_params.get('city_id'))
        )
        if city_id and city_id.isdigit():
            streets = self.queryset.filter(city=city_id)
            serializer = self.serializer_class(streets, many=True)
            return Response({'streets': serializer.data})
        else:
            raise

    def handle_exception(self, exc):
        return Response(status=400)


class ShopView(APIView):

    def get(self, request, *args, **kwargs):
        query = Shop.objects
        if 'street' in request.query_params:
            query = query.filter(street_id=request.query_params['street'])
        if 'city' in request.query_params:
            query = query.filter(city_id=request.query_params['city'])
        if 'open' in request.query_params:
            now_time = datetime.now().time()
            if int(request.query_params['open']):
                query = query.filter(opening_time__lte=now_time,
                             closing_time__gte=now_time)
            else:
                query = query.filter(Q(opening_time__gt=now_time) |
                             Q(closing_time__lt=now_time))

        if isinstance(query, QuerySet):
            query = query.all()

        serializer = ShopSerializer(query, many=True)
        return Response({'shops': serializer.data})

    def post(self, request, *args, **kwargs):
        data_shop = request.data.get('shop')
        serializer = ShopSerializer(data=data_shop)
        if serializer.is_valid(raise_exception=True):
            shop = serializer.save()
            return Response({'id': shop.id})

    def handle_exception(self, exc):
        return Response(status=400)
