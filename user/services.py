import os

import stripe

from lms_system.settings import STRIPE_API_KEY

STRIPE_BASE_URL = os.getenv("STRIPE_BASE_URL")
stripe.api_key = STRIPE_API_KEY
HEADERS = {
    "Authorization": f"Bearer {STRIPE_API_KEY}",
}


def create_stripe_product(course_title: str) -> str:
    """Создает продукт в Stripe и возвращает его ID."""
    product = stripe.Product.create(name=course_title)
    return product.id


def create_stripe_price(amount: int | float, product_id: str) -> str:
    """Создает цену в Stripe и возвращает её ID."""
    price = stripe.Price.create(
        currency="rub", unit_amount=int(amount * 100), product=product_id
    )
    return price.id


def create_stripe_session(price) -> tuple[str, str]:
    """Создает сессию оплаты в Stripe и возвращает (session_id, payment_url)."""
    session = stripe.checkout.Session.create(
        success_url="http://127.0.0.1:8000/",
        line_items=[{"price": price, "quantity": 1}],
        mode="payment",
    )
    return session.id, session.url


def retrieve_stripe_session(session_id: str) -> dict[str, str | None]:
    """Получает объект сессии из Stripe по её ID и возвращает статус оплаты."""
    session = stripe.checkout.Session.retrieve(session_id)
    return {"payment_status": session.payment_status, "status": session.status}
