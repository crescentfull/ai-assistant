from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib import messages

from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.views import OAuth2LoginView, OAuth2CallbackView
from allauth.socialaccount.helpers import render_authentication_error

from .gpt import ask_gpt
import logging

logger = logging.getLogger(__name__)

class CustomOAuth2LoginView(OAuth2LoginView):
    adapter_class = GoogleOAuth2Adapter

    def get_adapter(self, request):
        return self.adapter_class(request)

    def dispatch(self, request, *args, **kwargs):
        try:
            self.adapter = self.get_adapter(request)  # adapter 인스턴스를 설정
            return super().dispatch(request, *args, **kwargs)
        except Exception as e:
            logger.error(f"OAuth2LoginView error: {e}")
            messages.error(request, "An error occurred during the login process. Please try again.")
            return redirect('account_login')

class CustomOAuth2CallbackView(OAuth2CallbackView):
    adapter_class = GoogleOAuth2Adapter

    def get_adapter(self, request):
        return self.adapter_class(request)

    def dispatch(self, request, *args, **kwargs):
        try:
            self.adapter = self.get_adapter(request)  # adapter 인스턴스를 설정
            return super().dispatch(request, *args, **kwargs)
        except Exception as e:
            logger.error(f"OAuth2CallbackView error: {e}")
            messages.error(request, "An error occurred during authentication. Please try again.")
            return render_authentication_error(request)


def chat(request):
    """
    사용자가 GPT-3와 상호작용할 수 있는 뷰.
    """
    if request.method == 'POST':
        question = request.POST.get('question')
        answer = ask_gpt(question)
        logger.debug(f"User question: {question}, GPT-3 answer: {answer}")
        return render(request, 'chat.html', {'answer': answer})
    return render(request, 'chat.html')


def home(request):
    """
    홈 페이지를 렌더링하는 뷰.
    """
    logger.debug("Rendering home page")
    return render(request, 'home.html')

def custom_login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')
            return redirect('account_login')
    return render(request, 'login.html')

@login_required
def dashboard(request):
    """
    사용자 대시보드를 렌더링하는 뷰. 로그인된 사용자만 접근 가능.
    """
    logger.debug(f"User {request.user} accessed dashboard")
    return render(request, 'dashboard.html')