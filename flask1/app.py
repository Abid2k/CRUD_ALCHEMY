from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from os import environ
from dotenv import load_dotenv
from sqlalchemy import text

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://Servers:Abid@123@localhost:5432/SampleDB'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)
    
    with app.app_context():
        db.create_all()  # Create tables
        
    register_resources(app)
    return app

def register_resources(app):
    @app.route('/', methods=['GET'])
    def home():
        return render_template('index.html')

    @app.route('/users')
    def list_users():
        from models import User
        users = User.query.all()
        return render_template('users.html', users=users)

    @app.route('/user/create', methods=['GET', 'POST'])
    def create_user():
        from models import User
        if request.method == 'POST':
            try:
                new_user = User(
                    username=request.form['username'],
                    email=request.form['email']
                )
                db.session.add(new_user)
                db.session.commit()
                return redirect(url_for('list_users'))
            except Exception as e:
                return f'Error creating user: {str(e)}'
        return render_template('create_user.html')

    @app.route('/user/edit/<int:id>', methods=['GET', 'POST'])
    def edit_user(id):
        from models import User
        user = User.query.get_or_404(id)
        if request.method == 'POST':
            user.username = request.form['username']
            user.email = request.form['email']
            db.session.commit()
            return redirect(url_for('list_users'))
        return render_template('edit_user.html', user=user)

    @app.route('/user/delete/<int:id>')
    def delete_user(id):
        from models import User
        user = User.query.get_or_404(id)
        db.session.delete(user)
        db.session.commit()
        return redirect(url_for('list_users'))

if __name__ == "__main__":
    app = create_app()
    app.run('127.0.0.1', 5000, debug=True)