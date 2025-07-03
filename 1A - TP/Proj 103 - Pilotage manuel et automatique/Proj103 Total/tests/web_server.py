import http.server
import socketserver

PORT = 8000

html = """
<!DOCTYPE html>
<html>
	<head>
		<title>Premier test</title>
		<meta charset="utf-8">
	</head>
	<body id="app">
    	<button onclick="executerCommande('avancer')">Avancer</button>
    	<button onclick="executerCommande('stop')">Stop</button>
        <button onclick="executerCommande('reculer')">Reculer</button><br>
        <button onclick="executerCommande('gauche')">Gauche</button>
        <button onclick="executerCommande('droite')">Droite</button>
    	<div id="resultat"></div>
        
        <label for="curseur">Valeur :</label>
        <input type="range" id="curseur" min="0" max="100" value="50" oninput="changerValeur(this.value)">
        <div id="valeur">50</div>
        <br>
        <br>
        <button onclick="executerCommande('auto')">Auto</button><br>
        <button onclick="executerCommande('manuel')">Manuel</button>
	</body>
    <script>
    let commande_precedente = 'stop';
    function executerCommande(commande) {
        commande_precedente = commande;
        fetch("/" + commande + "/" + document.getElementById('valeur').innerText)
            .catch(error => {
                console.error(error);
            });
    }
    
    //const curseur = document.getElementById("curseur");
    //curseur.addEventListener('input', () => {
    //    executerCommande(commande_precendente);
    //    });
    
    document.addEventListener('keydown', function(event) {
                switch (event.key) {
                    case 'ArrowUp':
                        executerCommande('avancer');
                        break;
                    case 'ArrowDown':
                        executerCommande('reculer');
                        break;
                    case 'ArrowLeft':
                        executerCommande('gauche');
                        break;
                    case 'ArrowRight':
                        executerCommande('droite');
                        break;
                    case 'A' :
                        executerCommande('conduite_auto');
                    case ' ':
                        executerCommande('stop');
                        break;
                }
            })
    function changerValeur(valeur) {
                document.getElementById('valeur').innerText = valeur;
                executerCommande(commande);
                }
    </script>
</html>
"""

class MyHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        print(self.path)
        tab = self.path.split("/")
        print(tab)
        vitesse = 50
        if len(tab)>=3 and tab[2]!="":
            vitesse = int(tab[2])
        if tab[1] == 'avancer':
            print("avancer",vitesse)
        elif tab[1] == 'stop':
            print("stop")
        elif tab[1] == 'gauche':
            print("gauche",vitesse)
        elif tab[1] == 'droite':
            print("droite",vitesse)
        elif tab[1] == 'reculer':
            print("reculer",vitesse)
        elif tab[1] == 'auto':
            print("auto")
        elif tab[1] == 'manuel':
            print("manuel")
        else:
            result = "unknown command"
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(html.encode())

with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
    print("running")
    httpd.serve_forever()
