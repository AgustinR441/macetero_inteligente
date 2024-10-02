from flask import Flask, request, jsonify, render_template, redirect
from twilio.twiml.messaging_response import MessagingResponse
import sqlite3

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/insertar', methods=['GET'])
def insertar():
    return render_template('insertar.html')  

def get_ultima_temperatura():
    conn = sqlite3.connect('data.db')  
    cursor = conn.cursor()
    cursor.execute("SELECT temperatura FROM datos ORDER BY id DESC LIMIT 1")
    result = cursor.fetchone()
    conn.close()
    if result:
        return result[0]
    return None

def get_ultima_humedad():
    conn = sqlite3.connect('data.db') 
    cursor = conn.cursor()
    cursor.execute("SELECT humedadUp FROM datos ORDER BY id DESC LIMIT 1")
    result = cursor.fetchone()
    conn.close()
    if result:
        return result[0]
    return None

def get_ultima_agua():
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    cursor.execute("SELECT humedadSub FROM datos ORDER BY id DESC LIMIT 1")
    result = cursor.fecthone()
    conn.close()
    if result:
        return result[0]
    return None

@app.route('/webhook', methods=['POST'])
def webhook():
    mensajeLlegada = request.values.get('Body', '').lower()
    resp = MessagingResponse()
    msg = resp.message()

    if 'temperatura' in mensajeLlegada:
        temperatura = get_ultima_temperatura()
        if temperatura:
            msg.body(f"La temperatura actual es {temperatura}°C")
        else:
            msg.body("No se pudo obtener la temperatura. Verifica el servidor.")
    if 'humedad' in mensajeLlegada:
        humedad = get_ultima_humedad()
        if humedad:
            msg.body(f"La humedad actual es {humedad}%")
        else:
            msg.body("No se pudo obtener la humedad. Verifica el servidor.")
    if 'agua' in mensajeLlegada:
        agua = get_ultima_agua()
        if agua:
            msg.body(f"El nivel de agua actual es {agua}%")
        else:
            msg.body("No se pudo obtener el nivel de agua. Verifica el servidor.")
    if 'datos' in mensajeLlegada:
        temperatura = get_ultima_temperatura()
        humedad = get_ultima_humedad()
        agua = get_ultima_agua()

        if agua and temperatura and humedad:
            msg.body(f"Los datos de los sensores son: \n*Temperatura:* {temperatura}°C 
                     \n*Humedad:* {humedad}% 
                     \n*Agua:* {agua}%")
        else:
            msg.body("No se pudieron obtener los datos de los sensores. Verifica el servidor.")
            
    return str(resp)
        
@app.route('/send-data', methods=['POST'])
def send_data():
    temperatura = request.form['temperatura']
    humedadUp = request.form['humedadUp']
    humedadSub = request.form['humedadSub']
    fecha = request.form['fecha']
    hora = request.form['hora']

    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()

    # Consulta SQL
    cursor.execute("""
        INSERT INTO datos (temperatura, humedadUp, humedadSub, fecha, hora)
        VALUES (?, ?, ?, ?, ?);
    """, (temperatura, humedadUp, humedadSub, fecha, hora))

    conn.commit()
    conn.close()
    return redirect("/")

@app.route('/send-data-esp32', methods=['POST'])
def send_data_esp32():
    temperatura = request.form['temperatura']
    humedadUp = request.form['humedadUp']
    humedadSub = request.form['humedadSub']
    fecha = request.form['fecha']
    hora = request.form['hora']

    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()

    # Consulta SQL
    cursor.execute("""
        INSERT INTO datos (temperatura, humedadUp, humedadSub, fecha, hora)
        VALUES (?, ?, ?, ?, ?);
    """, (temperatura, humedadUp, humedadSub, fecha, hora))

    conn.commit()
    conn.close()
    return "Data ingresada correctamente."

@app.route('/get-data', methods=['GET'])
def get_data():
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM datos ORDER BY id DESC;')
    rows = cursor.fetchall()
    conn.close()
    return jsonify(rows)

@app.route('/eliminar-datos', methods=['GET'])
def eliminar_datos():
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM datos;')
    conn.commit()
    conn.close()
    return redirect("/")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True) # para permitir accesos locales
    #app.run(debug=True)
