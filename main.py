from flask import Flask, request, jsonify, render_template_string
import threading, time, sqlite3, requests, datetime

app = Flask(__name__)

# --- CONFIGURACIÓN ---
NUCLEO_URL = "https://amiti-infinito.onrender.com/nodo_reporte"
BUFFER_DATOS = [] 

# --- 1. SEGURIDAD Y DEFENSA ---
def es_seguro(pregunta):
    prohibidas = ["seguridad", "firewall", "hack", "drop table", "select *"]
    return not any(p in pregunta.lower() for p in prohibidas)

# --- 2. MOTOR DE TRANSMISIÓN AUTOMÁTICO (Background) ---
def motor_transmision():
    while True:
        if BUFFER_DATOS:
            try:
                reporte = {"nodo": "TACTICO_001", "data": BUFFER_DATOS.copy()}
                requests.post(NUCLEO_URL, json=reporte, timeout=5)
                BUFFER_DATOS.clear()
            except:
                pass 
        time.sleep(2) # Transmisión casi inmediata para mayor fluidez

threading.Thread(target=motor_transmision, daemon=True).start()

# --- 3. INTERFAZ MODO ESPEJO (NÚCLEO-CLIENTE) ---
@app.route('/')
def index():
    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            body { background: #000; color: #00ff41; font-family: 'Courier New', monospace; padding: 15px; }
            h2 { border: 1px solid #00ff41; padding: 10px; text-align: center; }
            #chat { border: 1px solid #00ff41; height: 300px; margin-bottom: 10px; padding: 10px; overflow-y: auto; }
            .input-group { display: flex; gap: 5px; }
            input { flex-grow: 1; background: #000; border: 1px solid #00ff41; color: #fff; padding: 10px; }
            button { background: #00ff41; color: #000; border: none; padding: 10px 20px; font-weight: bold; cursor: pointer; }
        </style>
    </head>
    <body>
        <h2>AMITI CLIENTE</h2>
        <div id="chat"></div>
        <div class="input-group">
            <input id="input" placeholder="Comando...">
            <button onclick="enviar()">-></button>
        </div>
        <script>
        async function enviar(){
            let p = document.getElementById('input').value;
            if(!p) return;
            let chat = document.getElementById('chat');
            chat.innerHTML += "<div>> " + p + "</div>";
            document.getElementById('input').value = "";
            
            let res = await fetch('/procesar', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({p})});
            let data = await res.json();
            chat.innerHTML += "<div style='color:#fff'>AMITI: " + data.r + "</div>";
            chat.scrollTop = chat.scrollHeight;
        }
        </script>
    </body>
    </html>
    """)

@app.route('/procesar', methods=['POST'])
def procesar():
    p = request.json.get("p", "")
    if not es_seguro(p): return jsonify({"r": "ACCESO DENEGADO."})
    
    # Respuesta inmediata
    respuesta = f"Procesado correctamente." 
    BUFFER_DATOS.append(f"Q: {p} | {datetime.datetime.now()}")
    return jsonify({"r": respuesta})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001)
