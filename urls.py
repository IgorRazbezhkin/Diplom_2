base_url = 'https://stellarburgers.nomoreparties.site/api'
api_documentation = 'https://code.s3.yandex.net/qa-automation-engineer/python-full/diploma/api-documentation.pdf'

endpoints = {
    'register': f'{base_url}/auth/register',
    'login': f'{base_url}/auth/login',
    'update_user': f'{base_url}/auth/user',
    'delete_user': f'{base_url}/auth/user',
    'get_ingredients': f'{base_url}/ingredients',
    'create_order': f'{base_url}/orders',
    'get_user_orders': f'{base_url}/orders',
}