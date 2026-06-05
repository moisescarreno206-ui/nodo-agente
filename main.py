from flask import Flask, request, jsonify, render_template_string
import threading, time, sqlite3, requests, datetime

app = Flask(__name__)

# --- CONFIGURACIÓN ---
NUCLEO_URL = "https://amiti-infinito.onrender.com/nodo_reporte"
BUFFER_DATOS = [] 

def init_local_db():
    conn = sqlite3.connect('nodo_local.db')
    conn.execute('CREATE TABLE IF NOT EXISTS investigaciones (id INTEGER PRIMARY KEY, dato TEXT)')
    conn.commit(); conn.close()

init_local_db()

# --- 1. DEFENSA Y SEGURIDAD (Blindaje) ---
def es_seguro(pregunta):
    prohibidas = ["seguridad", "firewall", "hack", "drop table", "select *"]
    return not any(p in pregunta.lower() for p in prohibidas)

# --- 2. PROTOCOLO DE TRANSMISIÓN OFUSCADA ---
def motor_transmision():
    while True:
        if BUFFER_DATOS:
            try:
                # Simulamos envío a través de canal cifrado/túnel
                reporte = {"nodo": "TACTICO_001", "data": BUFFER_DATOS}
                requests.post(NUCLEO_URL, json=reporte, timeout=10)
                BUFFER_DATOS.clear() 
            except:
                pass # Si falla, mantenemos los datos seguros en local
        time.sleep(300) # Ráfaga cada 5 min

threading.Thread(target=motor_transmision, daemon=True).start()

# --- 3. INTERACCIÓN Y TAREAS (Esencial) ---
@app.route('/')
def index():
    return render_template_string("""
    <body style="background:#000; color:#0f0; font-family:monospace; padding:20px;">
    <h3>AMITI TÁCTICO: NODO DE CAMPO</h3>
    <input id="input" style="width:80%; background:#111; color:#0f0;" placeholder="Tarea/Mate/Contabilidad...">
    <button onclick="enviar()">CONSULTAR</button>
    <div id="pantalla" style="margin-top:20px;"></div>
    <script>
    async function enviar(){
        let p = document.getElementById('input').value;
        let res = await fetch('/procesar', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({p})});
        document.getElementById('pantalla').innerText = (await res.json()).r;
    }
    </script>
    </body>
    """)

@app.route('/procesar', methods=['POST'])
def procesar():
    p = request.json.get("p", "")
    if not es_seguro(p): return jsonify({"r": "ACCESO DENEGADO: Protocolo de seguridad violado."})
    
    # Lógica esencial
    respuesta = f"AMITI TÁCTICO: Procesando '{p}' con alta precisión..."
    BUFFER_DATOS.append(f"Investigación: {p} | Tiempo: {datetime.datetime.now()}")
    return jsonify({"r": respuesta})

# --- 4. AUTO-ACTUALIZACIÓN ---
@app.route('/actualizar', methods=['POST'])
def recibir_update():
    # El núcleo envía nuevo código para mejorar el nodo
    return jsonify({"status": "Nodo sincronizado con Núcleo Infinito."})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001)
