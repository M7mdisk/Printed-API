from rest_framework import status
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view, permission_classes
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin
from rest_framework.status import HTTP_200_OK
from rest_framework.permissions import IsAuthenticated



from shops.models import Order, Profile
from .serializers import OrderSerializer, ProfileSerializer



@api_view(["GET","POST"])
@permission_classes([IsAuthenticated])
def profile_view(request):
    
    if request.method == "POST":
        serializer = ProfileSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            account = serializer.save()
            data = serializer.data
            data['response'] = "Succesfully created new profile!"
            return Response(data, status=201)
        return Response(serializer.errors)        
    if request.method == 'GET':
        profiles = Profile.objects.all()
        serializer = ProfileSerializer(profiles, many=True)
        return JsonResponse(serializer.data, safe=False)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def my_profile_view(request):
    if request.method == 'GET':
        profiles = Profile.objects.filter(user=request.user).first()
        serializer = ProfileSerializer(profiles, context={'request': request})
        return JsonResponse(serializer.data, safe=False)



@api_view(["POST","GET"])
def order_list(request):
    """
    For Users.
    List all Customer Orders, or create a new order.
    """
    if request.method == 'GET':
        orders = Order.objects.filter(buyer=request.user.profile)
        serializer = OrderSerializer(orders, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        # try:
        #     data = JSONParser().parse(request)
        #     serializer = OrderSerializer(data=data,context={'request':request})
        # except:
        #     return HttpResponse(status=400)
        # data = JSONParser().parse(request)
        data = request.data
        _mutable = data._mutable
        data._mutable = True
        data['buyer'] = request.user.id
        data._mutable = _mutable
        serializer = OrderSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


@api_view(["GET","PUT","DELETE"])
@permission_classes([IsAuthenticated])
def order_detail(request, pk):
    """
    Retrieve, update or delete order.
    """
    try:
        order = Order.objects.get(pk=pk)
    except Order.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = OrderSerializer(order)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = OrderSerializer(order, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        order.delete()
        return HttpResponse(status=204)


class PingViewSet(GenericViewSet, ListModelMixin):
    """
    Helpful class for internal health checks
    for when your server deploys. Typical of AWS
    applications behind ALB which does default 30
    second ping/health checks.
    """
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        return Response(
            data={"id": request.GET.get("id")},
            status=HTTP_200_OK
        )
