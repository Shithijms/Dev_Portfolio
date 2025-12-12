from django.shortcuts import render
from .models import BlockedIP

class BlockHackerMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # 1. Get the user's IP address
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')

        # 2. Check if this IP is in our Blacklist
        if BlockedIP.objects.filter(ip_address=ip).exists():
            # 3. If yes, show the custom "You are blocked" page immediately
            # We use status=403 (Forbidden)
            return render(request, 'blocked_hacker.html', status=403)

        # 4. If not blocked, let them pass
        response = self.get_response(request)
        return response