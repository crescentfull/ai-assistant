import openai
import logging

logger = logging.getLogger(__name__)

openai.api_key = 'your_openai_api_key'

def ask_gpt(question):
    """
    OpenAI GPT-3를 사용하여 질문에 대한 답변을 생성합니다.
    """
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=question,
            max_tokens=150
        )
        answer = response.choices[0].text.strip()
        logger.debug(f"GPT-3 response: {answer}")
        return answer
    except Exception as e:
        logger.error(f"Error getting response from GPT-3: {e}")
        raise
