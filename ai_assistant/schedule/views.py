from django.shortcuts import render
from django.contrib.auth.decorators import login_required
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

@login_required
def dashboard(request):
    """
    사용자 대시보드를 렌더링하는 뷰. 로그인된 사용자만 접근 가능.
    """
    logger.debug(f"User {request.user} accessed dashboard")
    return render(request, 'dashboard.html')