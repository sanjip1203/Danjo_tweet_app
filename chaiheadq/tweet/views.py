from django.shortcuts import render, get_object_or_404, redirect
from .models import Tweet
from .forms import TweetForm

# Home page view
def index(request):
    return render(request, 'index.html')

# List all tweets
def tweet_list(request):
    tweets = Tweet.objects.all().order_by('-created_at')
    return render(request, 'tweet_list.html', {'tweets': tweets})

# Create a new tweet
def tweet_create(request):
    if request.method == "POST":
        form = TweetForm(request.POST, request.FILES)
        if form.is_valid():
            tweet = form.save(commit=False)
            tweet.user = request.user
            tweet.save()
            return redirect('tweet_list')
    else:
        form = TweetForm()  # Ensure form is always defined

    return render(request, 'tweet_form.html', {'form': form})

# Edit an existing tweet
def tweet_edit(request, tweet_id):
    tweet = get_object_or_404(Tweet, pk=tweet_id, user=request.user)
    form = TweetForm(instance=tweet)  # Always initialize form

    if request.method == 'POST':
        form = TweetForm(request.POST, request.FILES, instance=tweet)
        if form.is_valid():
            form.save()  # No need to manually set `user`, it's already set
            return redirect('tweet_list')

    return render(request, 'tweet_form.html', {'form': form, 'tweet': tweet})

# Delete a tweet
def tweet_delete(request, tweet_id):
    tweet = get_object_or_404(Tweet, pk=tweet_id, user=request.user)
    if request.method == 'POST':
        tweet.delete()
        return redirect('tweet_list')

    return render(request, 'tweet_confirm_delete.html', {'tweet': tweet})
