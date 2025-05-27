from flask import Flask, session
from core.view import View
from controllers.main_controller import MainController

app = Flask(__name__)
app.secret_key = 'your-secret-key'  # Необходим для работы с сессиями

@app.route('/')
def home():
    view = View(['main', 'home'])
    controller = MainController(view)
    return controller.home_action()

if __name__ == '__main__':
    app.run(debug=True) 