import logging
from openai import AsyncOpenAI
from config import GPT_TOKEN


MODEL = 'gpt-4o-mini'

DEFAULT_PROMPT = 'Полезный ассистент-бот. Отвечай очень кратко, не более 4 предложений, можно короче.'


logger = logging.getLogger(__name__)

client = AsyncOpenAI(
    # This is the default and can be omitted
    api_key=GPT_TOKEN,
)


async def ask_gpt(user_message: str,
                  system_prompt: str = DEFAULT_PROMPT,
                  history: list = None) -> str:
    try:
        messages = [{'role': 'system', 'content': system_prompt}]

        if history:
            logger.info('История не пуста, добавляем её к будущему запросу %s', history)
            messages.append(history)

        messages.append({'role': 'user', 'content': user_message})
        response = await client.chat.completions.create(
            model=MODEL,
            messages=messages,
            max_tokens=1000,
            temperature=0.8
        )

        answer = response.choices[0].message.content
        logger.info('Получили ответ от chatgpt %s', answer)
        return answer
    except Exception as e:
        logger.error('Ошибка GPT %s', e)
        return 'Ошибка при обращении к GPT. Попробуй еще раз'








