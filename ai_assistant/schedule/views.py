from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .gpt import ask_gpt
import logging

logger = logging.getLogger(__name__)

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