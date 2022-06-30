import json

from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import ListView
from django.utils.timezone import now, timedelta
from django.db.models import Q

from .models import Todo


class TodoListView(ListView):
    model = Todo
    queryset = Todo.objects.filter(
        Q(datetime_completed__isnull=True)
        | Q(datetime_completed__gte=now() - timedelta(days=7))
    ).order_by('is_completed')
    context_object_name = 'todos'


def todo_create_view(request):
    if request.method == 'POST':
        Todo.objects.create(name=request.POST['name'])

    return redirect(reverse('todo_list_view'))


def todo_complete_view(request, pk):
    if request.method != 'POST':
        return JsonResponse({
            'success': False,
            'error': 'method not allowed'
        })

    todo = Todo.objects.get(pk=pk)
    data = json.loads(request.body)

    todo.is_completed = data['is_completed']
    todo.datetime_completed = now() if todo.is_completed else None
    todo.save()

    return JsonResponse({
        'success': True
    })
