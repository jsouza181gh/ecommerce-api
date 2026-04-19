import mercadopago
from app.config import MERCADOPAGO_ACCESS_TOKEN
from uuid import uuid4

def teste():
    sdk = mercadopago.SDK(MERCADOPAGO_ACCESS_TOKEN)

    request_options = mercadopago.config.RequestOptions()
    request_options.custom_headers = {
        'x-idempotency-key': str(uuid4())
    }

    payment_data = {
        "items": [
            {
                "id": "1234",
                "title": "Dummy Title",
                "quantity": 1,
                "currency_id": "BRL",
                "unit_price": 10,
            },
        ],
        # "back_urls": {
        #     "success": "https://test.com/success",
        #     "failure": "https://test.com/failure",
        #     "pending": "https://test.com/pending",
        # },
        # "auto_return": "all",
    }
    result = sdk.preference().create(payment_data, request_options)
    payment = result["response"]['init_point']

    print(payment)

#https://www.mercadopago.com.br/developers/pt/reference/online-payments/checkout-pro/preferences/create-preference/post

