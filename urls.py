BASE_URL = 'https://stellarburgers.nomoreparties.site/api'
API_DOCUMENTATION = 'https://code.s3.yandex.net/qa-automation-engineer/python-full/diploma/api-documentation.pdf'

ENDPOINTS = {
    'register': f'{BASE_URL}/auth/register',
    'login': f'{BASE_URL}/auth/login',
    'update_user': f'{BASE_URL}/auth/user',
    'delete_user': f'{BASE_URL}/auth/user',
    'get_ingredients': f'{BASE_URL}/ingredients',
    'create_order': f'{BASE_URL}/orders',
    'get_user_orders': f'{BASE_URL}/orders',
}