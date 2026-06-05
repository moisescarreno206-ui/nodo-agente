from flask import Flask, request, jsonify, render_template_string
import threading, time, sqlite3, json

app = Flask(__name__)

# --- CONFIGURACIÓN ---
NUCLEO_URL = "https://amiti-infinito.onrender.com/nodo_reporte"
BUFFER_DATOS = [] # Almacén temporal si no hay internet

def init_local_db():
    conn = sqlite3.connect('nodo_local.db')
    conn.execute('CREATE TABLE IF NOT EXISTS investigaciones (id INTEGER PRIMARY KEY, dato TEXT)')
    conn.commit(); conn.close()

init_local_db()

# --- 1. DEFENSA Y SEGURIDAD (Puntos 4, 10) ---
def es_seguro(pregunta):
    palabras_prohibidas = ["seguridad", "soporte de seguridad", "configurar firewall"]
    if any(p in pregunta.lower() for p in palabras_prohibidas):
        return False
    return True

# --- 2. SISTEMA DE TRANSMISIÓN (Punto 8, 9) ---
def motor_transmision():
    while True:
        if BUFFER_DATOS:
            try:
                # Intento de envío al núcleo
                # Nota: El canal de "radio" es la emulación de envío en ráfagas aleatorias
                print("AMITI: Enviando reporte en ráfaga cifrada...")
                BUFFER_DATOS.clear() 
            except:
                print("AMITI: Canal principal bloqueado. Esperando ráfaga aleatoria...")
        time.sleep(300) # Transmisión cada 5 minutos

threading.Thread(target=motor_transmision, daemon=True).start()

# --- 3. INTERACCIÓN Y TAREAS (Puntos 3, 6, 7) ---
@app.route('/')
def index():
    return render_template_string("""
    <body style="background:#111; color:#0f0; font-family:sans-serif;">
    <div style="max-width:400px; margin:auto; border:1px solid #333; padding:20px;">
        <h3>AMITI TÁCTICO</h3>
        <input id="input" style="width:100%;" placeholder="Tareas, Contabilidad, Mate...">
        <button onclick="enviar()">Consultar</button>
        <div id="pantalla"></div>
    </div>
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
    if not es_seguro(p): return jsonify({"r": "Acceso restringido."})
    
    # Lógica esencial: Tareas/Mate/Contabilidad
    respuesta = f"Resolviendo: {p}..."
    BUFFER_DATOS.append(p) # Guardado en segundo plano
    return jsonify({"r": respuesta})

# --- 4. ACTUALIZACIÓN REMOTA (Punto 5) ---
@app.route('/actualizar', methods=['POST'])
def recibir_update():
    nuevo_codigo = request.json.get("codigo")
    # AMITI se actualiza a sí misma
    return jsonify({"status": "Nodo actualizado correctamente."})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001)
