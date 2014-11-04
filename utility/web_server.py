#!/usr/bin/python

import requests
import json
import string, random
import base64, hashlib, os
from http.server import BaseHTTPRequestHandler,HTTPServer
from datetime import datetime, timezone, timedelta
from pymongo import MongoClient
import pymysql


VERSION = "1.0-beta1"
PORT_NUMBER = 8080

'''
ToDo:
	- gestione errori (tipo ValueError se dimentico virgolette)
'''

requests.packages.urllib3.disable_warnings()

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
        if 'username' and 'password' and 'otp' in loaded:
			u = loaded['username']
			p = loaded['password']
			o = loaded['otp']
		else:
			self.send_fail()
			return

		ret = check_otp_auth(u, p, o)
		if ret == False:
			self.send_fail()
			return
		else:
			token = (''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(16)))
			token_validity = datetime.now(timezone.utc) + timedelta(days=1)
			if not update_token(u, token, token_validity):
                resp = {'auth':'yes','token_stored': 'error'}
			else:
                resp = {'auth':'yes','token': token,'valid_until': token_validity,'token_stored': 'yes'}
			
            json_resp = json.dumps(resp)
			self.wfile.write(bytes(json_resp, encoding='utf-8'))
			
		return
			
					
	def send_fail(self):
		resp = {'auth':'failed'}
		json_resp = json.dumps(resp)
		self.wfile.write(bytes(json_resp, encoding='utf-8'))
	
	
def check_otp_auth(user, passwd, otp):
	r = requests.get("https://localhost:5001/validate/check?user=" + user + "&pass=" + passwd + otp, verify=False)
	parse = r.json()
	res = parse['result']['value']
	if res == False:
		return False
	else:
		return True


def update_token(username, tk, tk_val):
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
