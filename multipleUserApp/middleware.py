from django.contrib.auth import logout
from django.utils import timezone
from django.conf import settings
from django.shortcuts import redirect

class SessionTimeoutMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Skip expiration check for anonymous users
        if request.user.is_authenticated and 'last_activity' in request.session:
            last_activity = request.session['last_activity']
            expiration_time = last_activity + settings.SESSION_COOKIE_AGE
            if timezone.now() > expiration_time:
                # Redirect to login page or display session expired message
                return redirect('multipleUserApp:login')  # Assuming you have a URL named 'login'
        
        # Update last activity time only if session is modified
        if request.session.modified:
            request.session['last_activity'] = timezone.now()

        response = self.get_response(request)
        return response
