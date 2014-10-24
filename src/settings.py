#mongo instance
MONGO_HOST = 'localhost'
MONGO_PORT = 27017
MONGO_USERNAME = 'user'
MONGO_PASSWORD = 'pass'
MONGO_DBNAME = 'apitest'

#DEBUG = True

#/<domain>
RESOURCE_METHODS = ['GET', 'POST', 'DELETE']
#get: retrive all items from the specified <domain>
#post: create a new item in the specified <domain>
#delete: delete a specified <domain>

#/<domain>/<item>
ITEM_METHODS = ['GET', 'PATCH', 'PUT', 'DELETE']
#get: retrive a single <item>
#patch: partially update a specified <item>
#put: totally update a specified <item>
#delete: delete a specified <item>


accounts_schema = {
	'username': {
		'type': 'string',
		'minlength': 3,
		'maxlength': 50,
		'required': True,
		'unique': True,
	},
	'password': {
		'type': 'string',
		'minlength': 10,
		'maxlength': 256,
		'required': True,
	},
	'roles': {
		'type': 'list',
		'allowed': ['user'],
		'default': ['user'],
		'required': False,
	}
}

vm_schema = {
	'name': {
		'type': 'string',
		'required': True,
		'unique': True,
	},
	'os': {
		'type': 'string',
		'required': True,
	},
	'resources': {
		'type': 'dict',
		'schema': {
			'vCPU': { 'type': 'integer', 'required': True },
			'RAM': { 'type': 'integer', 'required': True },
			'Disk': { 'type': 'integer', 'required': True }
		},
	},
 	'actions': {
		'type': 'list',
		'allowed': [ "deploy", "halt", "reboot" ],
		'required': True
		
	}
}

accounts = {
	'additional_lookup': {
		'url': 'regex("[\w]+")',
		'field': 'username',
	},
	'cache_control': '',
	'cache_expires': 0,
	'auth_field': 'user_id',
	'public_methods': ['POST'],
	'public_item_methods': [],
	'resource_methods': ['GET'],
	'item_methods': ['PATCH','DELETE'],
	'extra_response_fields': ['token'],
	'schema': accounts_schema,
}

vms = {
	'additional_lookup': {
		'url': 'regex("[\w]+")',
		'field': 'name',
	},
	'cache_control': '',
	'cache_expires': 0,
	'public_methods': [],
	'public_item_methods': [],
	'auth_field': 'user_id',
	'schema': vm_schema,
}

DOMAIN = {
    'accounts': accounts,
    'vms': vms,
}
