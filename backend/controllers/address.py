from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from backend.models import Address, Tag
from backend.serializers import AddressSerializer, TagSerializer

from backend.controllers.controller_utils import HTTP_STATUS_CREATED, HTTP_STATUS_NO_CONTENT, HTTP_STATUS_BAD_REQUEST,\
    HTTP_STATUS_NOT_FOUND, HTTP_STATUS_METHOD_NOT_ALLOWED


@csrf_exempt
def address_detail(request, pk):
    """
    Retrieve or delete an address
    :param request:
    :param pk:
    :return: details of an address
    """
    try:
        address = Address.objects.get(pk=pk)
    except Address.DoesNotExist:
        return HttpResponse(status=HTTP_STATUS_NOT_FOUND)

    response = HttpResponse(status=HTTP_STATUS_METHOD_NOT_ALLOWED)
    if request.method == 'GET':
        response = __retrieve_address(address)
    elif request.method == 'DELETE':
        response = __delete_address(address)

    return response


@csrf_exempt
def address_list(request):
    """
    List all addresses or create a new one.
    :param request:
    :return: list of addresses
    """
    response = HttpResponse(status=HTTP_STATUS_METHOD_NOT_ALLOWED)
    if request.method == "GET":
        response = __list_addresses()
    elif request.method == "POST":
        response = __create_address(request)
    return response


@csrf_exempt
def address_tags(request, pk):
    """
    Retrieve an address' tags
    :param request:
    :param pk:
    :return: details of tags
    """
    try:
        address = Address.objects.get(pk=pk)
    except Address.DoesNotExist:
        return HttpResponse(status=HTTP_STATUS_NOT_FOUND)

    response = HttpResponse(status=HTTP_STATUS_METHOD_NOT_ALLOWED)
    if request.method == 'GET':
        response = __retrieve_tags_by_address(address)

    return response


def __retrieve_address(address):
    serializer = AddressSerializer(address)
    return JsonResponse(serializer.data)


def __delete_address(address):
    address.delete()
    return HttpResponse(status=HTTP_STATUS_NO_CONTENT)


def __list_addresses():
    addresses = Address.objects.all()
    serializer = AddressSerializer(addresses, many=True)
    return JsonResponse(serializer.data, safe=False)


def __create_address(request):
    data = JSONParser().parse(request)
    serializer = AddressSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return JsonResponse(serializer.data, status=HTTP_STATUS_CREATED)
    return JsonResponse(serializer.errors, status=HTTP_STATUS_BAD_REQUEST)


def __retrieve_tags_by_address(address):
    tags = Tag.objects.filter(address=address)
    serializer = TagSerializer(tags, many=True)
    return JsonResponse(serializer.data, safe=False)
