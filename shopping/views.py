import json
from datetime import timedelta

from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from django.utils import timezone
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from shopping.serializers import ItemSerializer

from .forms import ShoppingForm
from .models import Item


class ItemView(View):

    def get(self, request):
        items = Item.objects.filter(is_purchased=False).order_by("created_at")
        two_weeks_ago = timezone.now() - timedelta(days=14)
        purchased = Item.objects.filter(is_purchased=True, purchased_at__gt=two_weeks_ago).order_by(
            '-purchased_at', 'created_at')
        if not purchased.exists():
            purchased = Item.objects.filter(is_purchased=True).order_by(
                '-purchased_at', 'created_at')[:20]
        datalist = Item.objects.all().values('name').distinct().order_by('name')
        response = {
            "items": items,
            "purchased": purchased,
            "form": ShoppingForm(),
            "datalist": datalist,
        }
        return render(request, "shopping/index.html", response)

    def post(self, request):
        data = json.loads(request.body)
        form = ShoppingForm(data)
        if form.is_valid():
            item = Item(
                name=form.cleaned_data["item"],
                added_by=request.user if request.user.is_authenticated else None,
            )
            item.save()
        else:
            return JsonResponse({"success": False, "error": form.errors})

        return JsonResponse({"success": True})


class ItemPurchaseView(View):

    def put(self, request, item_id):
        item = Item.objects.get(pk=item_id)
        item.is_purchased = True
        item.purchased_at = timezone.now()
        item.purchased_by = request.user if request.user.is_authenticated else None
        item.save()
        return JsonResponse({"success": True})


class ItemDeleteView(View):

    def delete(self, request, item_id):
        item = Item.objects.get(pk=item_id)
        item.delete()
        return JsonResponse({"success": True})


class ItemRestoreView(View):

    def put(self, request, item_id):
        item = Item.objects.get(pk=item_id)
        item.is_purchased = False
        item.purchased_at = None
        item.purchased_by = None
        item.save()
        return JsonResponse({"success": True})


class ItemListAPIView(APIView):

    def get(self, request):
        items = Item.objects.filter(is_purchased=False).order_by("created_at")

        this_week = timezone.now() - timedelta(days=7)
        purchases = Item.objects.filter(is_purchased=True, purchased_at__gt=this_week).order_by(
            '-purchased_at', 'created_at')

        datalist = Item.objects.all().values('name').distinct().order_by('name')
        response = {
            "items": ItemSerializer(items, many=True).data,
            "purchases": ItemSerializer(purchases, many=True).data,
            "datalist": datalist,
        }
        return Response(response)

    def post(self, request):
        item = ItemSerializer(data=request.data)
        if item.is_valid():
            item.save()
            return Response(item.data, status=status.HTTP_201_CREATED)
        return Response(item.errors, status=status.HTTP_400_BAD_REQUEST)


class ItemDetailAPIView(APIView):

    def put(self, request, item_id):
        try:
            item = Item.objects.get(pk=item_id)
        except Item.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if (request.data['is_purchased'] == True):
            item.is_purchased = True
            item.purchased_at = timezone.now()
            item.purchased_by = request.user if request.user.is_authenticated else None
        else:
            item.is_purchased = False
            item.purchased_at = None
            item.purchased_by = None
        if "store" in request.data:
            item.store = request.data['store']
        if "name" in request.data:
            item.name = request.data['name']
        item.save()
        return Response(ItemSerializer(item).data)

    def delete(self, request, item_id):
        try:
            item = Item.objects.get(pk=item_id)
        except Item.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

