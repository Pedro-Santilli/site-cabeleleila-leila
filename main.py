from flask import Flask
from routes.auth import auth_bp
from routes.agendamento import agendamento_bp
from routes.admin import admin_bp
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)  

app.register_blueprint(auth_bp)
app.register_blueprint(agendamento_bp)
app.register_blueprint(admin_bp)

if __name__ == '__main__':
    app.run(debug=True)