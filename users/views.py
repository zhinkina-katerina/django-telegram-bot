from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import View


class UserProfile(LoginRequiredMixin, View):
    login_url = '/auth/login/'

    def get(self, request, *args, **kwargs):
        context = {
            'user': request.user
        }
        return render(request, 'user_profile.html', context)
