from flask import Flask, request, jsonify, render_template, redirect
import sqlite3

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/insertar', methods=['GET'])
def insertar():
    return render_template('insertar.html')  

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
