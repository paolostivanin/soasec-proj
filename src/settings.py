#mongo instance
MONGO_HOST = 'localhost'
MONGO_PORT = 27017
MONGO_USERNAME = 'user'
MONGO_PASSWORD = 'pass'
MONGO_DBNAME = 'apitest'

#DEBUG = True

#/...
RESOURCE_METHODS = ['GET', 'POST', 'DELETE']

#/.../<id>
ITEM_METHODS = ['GET', 'PATCH', 'PUT', 'DELETE']

schema = {
	'username': {
		'type': 'string',
		'required': True,
	},
	'password': {
		'type': 'string',
		'required': True,
	},
	'roles': {
		'type': 'list',
		'allowed': ['user', 'superuser', 'admin'],
		'required': True,
	},
	'token': {
		'type': 'string',
		'required': True,
	}
}

accounts = {
    'additional_lookup': {
        'url': 'regex("[\w]+")',
        'field': 'username'
    },
    'cache_control': '',
    'cache_expires': 0,
    'allowed_roles': ['admin', 'superuser', 'user'],
    'extra_response_fields': ['token'],
    'schema': schema
}

DOMAIN = {
    'accounts': accounts,
}
