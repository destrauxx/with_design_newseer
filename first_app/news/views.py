from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.contrib.auth.decorators import login_required, permission_required
from .forms import NewsModelForm
from news.models import News



def read(request, *args, **kwargs):
    qs = News.objects.all()
    context = {'news_list': qs}
    return render(request, 'read.html', context)
def index(request, *args, **kwargs):
    return render(request, 'index.html')
    
def detail_view(request, pk):
    try:
        obj = News.objects.get(id=pk)
    except News.DoesNotExist:
        raise Http404
    return render(request, 'news/detail.html', {'single_object': obj})

@login_required
@permission_required('user.is_staff', raise_exception=True)
def create_view(request, *args, **kwargs):
    form = NewsModelForm(request.POST or None)
    context = {'form': form}
    if form.is_valid():
        data = form.cleaned_data
        News.objects.create(**data)
    return render(request, 'forms.html', context)


@login_required
@permission_required('user.is_staff')
def edit_view(request, pk):
    try:
        obj = News.objects.get(id=pk)
    except News.DoesNotExist:
        raise Http404
    if request.method == 'POST':
        form = NewsModelForm(request.POST, instance = obj)
        if form.is_valid():
            edited_obj = form.save(commit=False)
            edited_obj.save()
    else:
        form = NewsModelForm(instance=obj)

    return render(request, 'edit_news_form.html', {'single_object' : obj, 'form': form})