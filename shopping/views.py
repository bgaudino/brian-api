import json
from datetime import timedelta

from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from django.utils import timezone

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
