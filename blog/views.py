from django.shortcuts import render,get_object_or_404
from .models import Post
from django.utils import timezone
from .forms import Postform
from django.shortcuts import redirect
# Create your views here.


def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    context ={
        'posts': posts
    }
    return render(request,'blog/post_list.html',context)

def post_detail(request,pk):
    post = get_object_or_404(Post,pk=pk)
    context = {
        'post':post
    }
    return render(request,'blog/post_detail.html',context)

def post_new(request):
    if request.method == "POST":
        form = Postform(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = Postform()
        context ={
        'form':form
        }
        return render(request,'blog/post_edit.html',context)

def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = Postform(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = Postform(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})
