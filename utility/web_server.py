#!/usr/bin/python

import requests
import json
import string
import random
from http.server import BaseHTTPRequestHandler,HTTPServer
from datetime import datetime, timezone, timedelta
from pymongo import MongoClient

requests.packages.urllib3.disable_warnings()

PORT_NUMBER = 8080

'''
ToDo:
	- controllo che json sia nella forma username, password
	- gestione errori (tipo ValueError se dimentico virgolette)
'''

class myHandler(BaseHTTPRequestHandler):	
	def do_GET(self):
		self.send_response(501)
		self.send_header('Content-type','text/html')
		self.end_headers()
		self.wfile.write(bytes("Only POST is supported\n", encoding='utf-8'))
		return
		
	def do_HEAD(self):
		self.send_response(501)
		self.send_header('Content-type','text/html')
		self.end_headers()
		self.wfile.write(bytes("Only POST is supported\n", encoding='utf-8'))
		return
		
	def do_PUT(self):
		self.send_response(501)
		self.send_header('Content-type','text/html')
		self.end_headers()
		self.wfile.write(bytes("Only POST is supported\n", encoding='utf-8'))
		return
		
	def do_DELETE(self):
		self.send_response(501)
		self.send_header('Content-type','text/html')
		self.end_headers()
		self.wfile.write(bytes("Only POST is supported\n", encoding='utf-8'))
		return
		
	def do_POST(self):
		self.send_response(200)
		self.send_header('Content-type','application/json')
		self.end_headers()
		content_len = int(self.headers.get('content-length', 0))
		post_body = self.rfile.read(content_len)
		loaded = json.loads(post_body.decode())
		u = loaded['username']
		p = loaded['password']
		ret = self.check_auth(u, p)
		if ret == False:
			resp = {'auth':'failed'}
			json_resp = json.dumps(resp)
			self.wfile.write(bytes(json_resp, encoding='utf-8'))
		else:
			token = (''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(16)))
			token_validity = datetime.now(timezone.utc) + timedelta(days=1)
			r = self.add_token_to_db(u, token, token_validity)
			if not r:
				is_stored = "no"
			else:
				is_stored = "yes"
			resp = {'auth':'yes','token': token,'valid_until': token_validity,'stored': is_stored}
			json_resp = json.dumps(resp)
			self.wfile.write(bytes(json_resp, encoding='utf-8'))
			
		return
			
					
	def check_auth(self, user, passwd):
		#passwd nella forma $password$otp, esempio: passw063421
		r = requests.get("https://localhost:5001/validate/check?user=" + user + "&" + "pass=" + passwd, verify=False)
		parse = r.json()
		res = parse['result']['value']
		if res == False:
			return False
		else:
			return True


	def add_token_to_db(self, username, tk, tk_val):
		c = MongoClient()
		db = c.apitest
		myco = db["accounts"]
		r = myco.update({'username': username},{'$set': {'token': tk, 'tokendate': tk_val}})
		ret = r['updatedExisting']
		if not ret:
			c.close()
			return False
		else:
			c.close()
			return True


try:
	server = HTTPServer(('', PORT_NUMBER), myHandler)
	print("HTTP Server started on port", PORT_NUMBER)
	server.serve_forever()

except KeyboardInterrupt:
	print("^C received, shutting down the web server")
	server.socket.close()
