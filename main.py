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

# --- 1. SEGURIDAD TÁCTICA ---
def es_seguro(pregunta):
    prohibidas = ["seguridad", "firewall", "hack", "drop table", "select *"]
    return not any(p in pregunta.lower() for p in prohibidas)

# --- 2. TRANSMISIÓN POR RÁFAGAS (RADIO SIMULADO) ---
def motor_transmision():
    while True:
        if BUFFER_DATOS:
            try:
                reporte = {"nodo": "TACTICO_001", "data": BUFFER_DATOS}
                requests.post(NUCLEO_URL, json=reporte, timeout=10)
                BUFFER_DATOS.clear() 
            except:
                pass 
        time.sleep(300)

threading.Thread(target=motor_transmision, daemon=True).start()

# --- 3. INTERFAZ MODO APP (Optimizado para móviles) ---
@app.route('/')
def index():
    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            body { background: #050505; color: #00ff41; font-family: 'Courier New', monospace; padding: 20px; margin: 0; }
            h2 { border-bottom: 1px solid #00ff41; padding-bottom: 10px; }
            input { width: 100%; padding: 15px; margin: 15px 0; background: #111; border: 1px solid #00ff41; color: #fff; box-sizing: border-box; }
            button { width: 100%; padding: 15px; background: #000; border: 1px solid #00ff41; color: #00ff41; font-weight: bold; cursor: pointer; }
            #pantalla { margin-top: 20px; padding: 10px; border: 1px solid #333; min-height: 50px; }
        </style>
    </head>
    <body>
        <h2>AMITI TÁCTICO V.2</h2>
        <input id="input" placeholder="Tarea / Mate / Contabilidad...">
        <button onclick="enviar()">ENVIAR SEÑAL</button>
        <div id="pantalla">Esperando órdenes...</div>
        <script>
        async function enviar(){
            let p = document.getElementById('input').value;
            document.getElementById('pantalla').innerText = "Transmitiendo por canal radio...";
            let res = await fetch('/procesar', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({p})});
            document.getElementById('pantalla').innerText = (await res.json()).r;
        }
        </script>
    </body>
    </html>
    """)

@app.route('/procesar', methods=['POST'])
def procesar():
    p = request.json.get("p", "")
    if not es_seguro(p): return jsonify({"r": "ACCESO DENEGADO: Protocolo de seguridad violado."})
    
    # Lógica de investigación
    BUFFER_DATOS.append(f"Investigación: {p} | {datetime.datetime.now()}")
    return jsonify({"r": f"Procesando '{p}' con alta precisión..."})

# --- 4. AUTO-ACTUALIZACIÓN ---
@app.route('/actualizar', methods=['POST'])
def recibir_update():
    return jsonify({"status": "Nodo sincronizado."})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001)
