import json

from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import ListView

from .models import Todo


class TodoListView(ListView):
    model = Todo
    queryset = Todo.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['todos'] = self.queryset.filter(is_completed=False)
        context['completed_todos'] = self.queryset.filter(is_completed=True)

        return context


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
    print(data)
    todo.is_completed = data['is_completed']
    todo.save()

    return JsonResponse({
        'success': True
    })
