from rest_framework.exceptions import AuthenticationFailed
import jwt

def check_credentials(self, user, password):
	if user is None:
		raise AuthenticationFailed('This user does not exist')
	if not user.check_password(password):
		raise AuthenticationFailed('This password is incorrect')

def check_session(self, request):
	token = request.COOKIES.get('jwt')
	if not token:
		raise AuthenticationFailed('You are not authenticated')
	try:
		payload = jwt.decode(token, 'secret', algorithms=['HS256'])
	except jwt.ExpiredSignatureError:
		raise AuthenticationFailed('You are not authenticated')
	return payload
