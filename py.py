from flask import Flask, render_template, request, session, redirect, url_for
import random

app = Flask(__name__)
# Clave secreta necesaria para usar session en Flask
app.secret_key = "clave_secreta_futurista"

class JuegoAdivinanza:
    def __init__(self, limite_inferior=1, limite_superior=100):
        self.limite_inferior = limite_inferior
        self.limite_superior = limite_superior

    def nuevo_numero(self):
        return random.randint(self.limite_inferior, self.limite_superior)

# Instancia global del juego
juego = JuegoAdivinanza(1, 100)

@app.route('/', methods=['GET', 'POST'])
def index():
    # Si no hay número secreto en la sesión, inicializamos la partida
    if 'numero_secreto' not in session:
        session['numero_secreto'] = juego.nuevo_numero()
        session['intentos'] = 0
        session['mensaje'] = "Inicia el protocolo. Ingresa un número del 1 al 100."
        session['ganado'] = False

    if request.method == 'POST':
        # Si el usuario presiona "Reiniciar"
        if 'reiniciar' in request.form:
            session.clear()
            return redirect(url_for('index'))

        # Si el usuario envía un número
        try:
            intento = int(request.form.get('numero'))
            session['intentos'] += 1

            if intento < session['numero_secreto']:
                session['mensaje'] = f" El número secreto es MAYOR que {intento}."
            elif intento > session['numero_secreto']:
                session['mensaje'] = f" El número secreto es MENOR que {intento}."
            else:
                session['mensaje'] = f" ¡ACCESO CONCEDIDO! Adivinaste el número en {session['intentos']} intentos."
                session['ganado'] = True
        except (ValueError, TypeError):
            session['mensaje'] = " Error de entrada: Ingresa un número entero válido."

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)