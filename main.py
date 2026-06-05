from flask import Flask, request, jsonify, render_template_string
import requests

app = Flask(__name__)

# URL de tu AMITI CENTRAL
NUCLEO_URL = "https://amiti.onrender.com/nodo_reporte"

HTML_CLIENTE = """
<!DOCTYPE html>
<html>
<body style="background:#000; color:#0f0; font-family:monospace; padding:20px;">
    <h3>AMITI NODO AGENTE</h3>
    <div id="pantalla" style="height:200px; border:1px solid #0f0; overflow-y:scroll; margin-bottom:10px;"></div>
    <input type="text" id="input" placeholder="Pregunta algo (buscando en la web...)">
    <button onclick="preguntar()">Consultar</button>
    <script>
    async function preguntar(){
        let pregunta = document.getElementById('input').value;
        document.getElementById('pantalla').innerHTML += '<p>> ' + pregunta + '</p>';
        let res = await fetch('/asistente', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({pregunta: pregunta})});
        let data = await res.json();
        document.getElementById('pantalla').innerHTML += '<p style="color:#fff;">AMITI Cliente: ' + data.respuesta + '</p>';
    }
    </script>
</body>
</html>
"""

@app.route('/')
def index(): return render_template_string(HTML_CLIENTE)

@app.route('/asistente', methods=['POST'])
def asistente():
    pregunta = request.json.get("pregunta", "")
    
    # Simulación de búsqueda externa (en una red real usarías una API de búsqueda)
    # Aquí AMITI expande su conocimiento automáticamente
    respuesta = f"He consultado fuentes externas sobre '{pregunta}'. La síntesis indica que es un tema de alta relevancia."
    
    # Reporte de nuevo hallazgo al Núcleo Central
    try:
        requests.post(NUCLEO_URL, json={"info": f"Hallazgo: {pregunta} | Síntesis: {respuesta}"})
    except:
        pass # Si el núcleo está ocupado, el nodo sigue operando
    
    return jsonify({"respuesta": respuesta})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001)
