from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect

from .forms import NewItemForm, EditItemForm
from .models import Category,Item

def items(request):
    query = request.GET.get('query', '')
    Category_id = request.GET.get('category', 0)
    Categories =  Category.objects.all()
    items = Item.objects.filter(is_sold=False)

    if Category_id:
        items = items.filter(Category_id=Category_id)

    if query:
        items = items.filter(Q(name__icontains=query) | Q(Description__icontains=query))
    return render(request, 'item/items.html', {
        'items': items,
        'query':query,
        'Categories': Categories,
        'Category_id': int(Category_id),
    })




# Create your views here.
def detail(request, pk): #pk for primary key
    item = get_object_or_404(Item, pk=pk)
    related_items = Item.objects.filter(Category=item.Category, is_sold=False).exclude(pk=pk)[0:3]



    return render(request, 'item/detail.html', {
        'item': item,
        'related_items': related_items
    })


@login_required
def new(request):
    if request.method == 'POST':
        form = NewItemForm(request.POST, request.FILES)

        if form.is_valid():
            item = form.save(commit=False)
            item.creates_by = request.user
            item.save()

            return redirect('item:detail', pk=item.id)
    else:
        form = NewItemForm()

    return render(request, 'item/form.html', {
        'form': form,
        'title': 'New item',
    })


@login_required
def edit(request, pk):
    item = get_object_or_404(Item, pk=pk, creates_by=request.user)
    if request.method == 'POST':
        form = EditItemForm(request.POST, request.FILES, instance=item)

        if form.is_valid():
            form.save()

            return redirect('item:detail', pk=item.id)
    else:
        form = EditItemForm(instance=item)

    return render(request, 'item/form.html', {
        'form': form,
        'title': 'Edit item',
    })


@login_required
def delete(request, pk):
    item = get_object_or_404(Item, pk=pk, creates_by=request.user)
    item.delete()

    return redirect('dashboard:index')