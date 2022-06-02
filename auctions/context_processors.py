from .models import Watchlist


def watchlist_count(request):
    if request.user.is_authenticated:
        user_watchlist = Watchlist.objects.filter(user=request.user)
        if user_watchlist:
            watchlist = Watchlist.objects.get(user=request.user)
            user_lists = watchlist.listings.all()
            return { "watchlist": watchlist, "user_lists": user_lists }
        
    return {}