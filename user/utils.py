def jwt_response_payload_handler(token, user=None, request=None):
    return {
        'token': token,
        'user': {
            'username': user.username,
            'user_id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email
        }
    }