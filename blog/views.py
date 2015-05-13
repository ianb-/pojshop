from django.shortcuts import render
from blog.models import Article
from blog.forms import ArticleForm
from django.shortcuts import redirect
from django.http import HttpResponse

def index(request):
	articles = Article.objects.order_by('-created')[:5]
	return render(request, 'blog/index.html', {'articles': articles})

def new(request):
	if request.user.is_authenticated():
		if request.method == 'POST':
			form = ArticleForm(request.POST)
			if form.is_valid():
				blag = form.save(commit=False)
				blag.author = request.user
				blag.save()
				return index(request)
			else:
				print form.errors
		else:	
			form = ArticleForm()
	else:
		return HttpResponse("You must be an autheticated user to be here.")
	return render(request, 'blog/new.html', {'form': form})

def article(request, article_slug):
	context = {}
	try:
		context['article'] = Article.objects.get(slug=article_slug)
	except Article.DoesNotExist:
		context['error'] = "Article not found"
	return render(request, 'blog/article.html', context)