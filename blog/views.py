from django.shortcuts import render
from django.utils import timezone
from .models import Post

# Create your views here.
def post_list(request):
    posts = Post()
    if (request.GET.get('subject_id') and request.GET.get('city_name')):
        if (request.GET.get('street_name')):
            addresses = posts.addresses(request.GET['subject_id'], request.GET['city_name'], request.GET['street_name'])
        else:
            addresses = posts.addresses(request.GET['subject_id'], request.GET['city_name'])

        return render(request, 'blog/post_list.html', {'addresses': addresses})
    else:
        return render(request, 'blog/post_list.html', {'addresses': {}})

