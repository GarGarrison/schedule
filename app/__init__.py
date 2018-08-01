from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config')

db = SQLAlchemy(app)

from app.controllers.AdminController import admin_module
from app.controllers.MainController import main_module

app.register_blueprint(main_module)
app.register_blueprint(admin_module)

db.create_all()

# print(app.url_map)

if __name__ == "__main__":
    app.run(host="0.0.0.0")
