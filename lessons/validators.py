import re
from urllib.parse import urlparse

from rest_framework.serializers import ValidationError

ALLOWED_DOMAINS = {
    "youtube.com",
    "://www.youtube.com",
    "://m.youtube.com",
    "youtu.be",
}


def validate_only_youtube(value: str) -> None:
    """Проверяет, что в переданном тексте нет ссылок на сторонние ресурсы,
    кроме youtube.com."""
    if not value or not isinstance(value, str):
        return

    # Находим все ссылки в тексте
    urls = re.findall(r'https?://[^\s<>"\'\)\]]+', value)

    for url in urls:
        domain = urlparse(url).netloc.lower()
        if domain not in ALLOWED_DOMAINS:
            raise ValidationError(
                f'Запрещенная ссылка: {url}". Разрешены только ссылки на YouTube.'
            )
