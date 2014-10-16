#mongo instance
MONGO_HOST = 'localhost'
MONGO_PORT = 27017
MONGO_USERNAME = 'user'
MONGO_PASSWORD = 'pass'
MONGO_DBNAME = 'apitest'

#DEBUG = True

#/accounts
RESOURCE_METHODS = ['GET', 'POST', 'DELETE']

#/accounts/<id>
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

schemavm = {
	'name': {
		'type': 'string',
		'required': True,
	},
}

accounts = {
    'additional_lookup': {
        'url': 'regex("[\w]+")',
        'field': 'username'
    },
    'cache_control': '',
    'cache_expires': 0,
    'allowed_roles': ['admin', 'superuser'],
    'extra_response_fields': ['token'],
    'public_methods': [],
    'schema': schema
}

vms = {
    'additional_lookup': {
        'url': 'regex("[\w]+")',
        'field': 'name'
    },
    'cache_control': '',
    'cache_expires': 0,
    'allowed_roles': ['user', 'superuser', 'admin'],
    'public_methods': ['GET'],
    'schema': schemavm
}

DOMAIN = {
    'accounts': accounts,
    'vms': vms,
}
