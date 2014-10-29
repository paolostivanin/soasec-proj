#!/usr/bin/python

import requests
import json
from http.server import BaseHTTPRequestHandler,HTTPServer

requests.packages.urllib3.disable_warnings()
PORT_NUMBER = 8080

'''
ToDo:
	- controllo che json sia nella forma username, password
	- head, put, delete, ecc negate (tipo GET)
	- gestione errori (tipo ValueError se dimentico virgolette)
	- generare token se auth ok e restituirlo
	- risposta in formato JSON
	- inserire token nel DB mongo
'''

class myHandler(BaseHTTPRequestHandler):	
	#Handler for the GET requests
	def do_GET(self):
		self.send_response(200)
		self.send_header('Content-type','text/html')
		self.end_headers()
		self.wfile.write(bytes("Only POST request is supported\n", encoding='utf-8'))
		return
		
	def do_POST(self):
		self.send_response(200)
		self.send_header('Content-type','text/html')
		self.end_headers()
		content_len = int(self.headers.get('content-length', 0))
		post_body = self.rfile.read(content_len)
		loaded = json.loads(post_body.decode())
		u = loaded['username']
		p = loaded['password']
		ret = self.check_auth(u, p)
		if ret == False:
			self.wfile.write(bytes("Not Auth\n", encoding='utf-8'))
		else:
			self.wfile.write(bytes("Auth\n", encoding='utf-8'))
				
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



try:
	server = HTTPServer(('', PORT_NUMBER), myHandler)
	print("Started httpserver on port 8080")
	server.serve_forever()

except KeyboardInterrupt:
	print("^C received, shutting down the web server")
	server.socket.close()
