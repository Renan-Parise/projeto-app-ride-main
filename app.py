from flask import Flask, render_template, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from flask_bcrypt import Bcrypt
from flask import flash
from routes import configure_routes
import requests

app = Flask(__name__)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

from models import User

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
    
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)

class RegisterForm(FlaskForm):
    username = StringField(validators=[
                           InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Nome de usuário"})

    email = StringField(validators=[
        InputRequired(), Length(max=120)], render_kw={"placeholder": "Email"})


    password = PasswordField(validators=[
                             InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Senha"})

    submit = SubmitField('Register')

    def validate_username(self, username):
        existing_user_username = User.query.filter_by(
            username=username.data).first()
        if existing_user_username:
            flash('Esse nome de usuário já existe. Por favor, escolha outro.')
            raise ValidationError(
                'Este nome de usuário já existe. Por favor, escolha outro.')

class LoginForm(FlaskForm):
    username = StringField(validators=[
                           InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Nome de usuário"})

    password = PasswordField(validators=[
                             InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Senha"})

    submit = SubmitField('Login')

    def validate_password(self, password):
        user = User.query.filter_by(username=self.username.data).first()
        if user and not bcrypt.check_password_hash(user.password, password.data):
            flash('Senha ou usuário incorreto. Por favor, tente novamente.', 'error')

@app.route('/home')
def index():
    return render_template('index.html')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for('dashboard'))
    return render_template('login.html', form=form)


@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    api_key = 'f7b2fd2be3e4a889b62d3ee745233a91'
    city = 'Videira'
    country_code = 'BR'
    api_url = f'http://api.openweathermap.org/data/2.5/weather?q={city},{country_code}&appid={api_key}&units=metric'
    response = requests.get(api_url)
    
    if response.status_code == 200:
        data = response.json()
        temperature = round(data['main']['temp'])
        weather_condition = data['weather'][0]['main']

        weather_translation = {
            'Clear': 'Limpo',
            'Clouds': 'Nublado',
            'Rain': 'Chovendo',
            'Snow': 'Nevando',
            'Drizzle': 'Garoa',
            'Thunderstorm': 'Tempestade',
            'Mist': 'Neblina',
            'Fog': 'Nevoeiro',
            'Haze': 'Nevoeiro Seco',
            'Smoke': 'Fumaça',
            'Dust': 'Poeira',
            'Sand': 'Areia',
            'Ash': 'Cinzas Vulcânicas',
            'Squalls': 'Rajadas de Vento',
            'Tornado': 'Tornado',
        }
        
        weather_condition = weather_translation.get(weather_condition, weather_condition)

        goodToGo = ''
        if weather_condition == 'Limpo':
            goodToGo = 'O tempo está limpo. É um ótimo dia para andar de bicicleta!'
        elif weather_condition == 'Nublado':
            goodToGo = 'O tempo está nublado. Verifique a possibilidade de chuva antes de sair.'
        elif weather_condition == 'Chovendo':
            goodToGo = 'O tempo está chuvoso. Não é um bom dia para andar de bicicleta!'
        elif weather_condition == 'Nevando':
            goodToGo = 'O tempo está nevando. Não é um bom dia para andar de bicicleta!'
        else:
            goodToGo = 'O tempo está com ' + weather_condition + '. Verifique a possibilidade de chuva antes de sair.'

        return render_template('dashboard.html', username=current_user.username, temperature=temperature, weather_condition=weather_condition, goodToGo=goodToGo)
    else:
        return render_template('dashboard.html', username=current_user.username)
    
@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        new_user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))

    return render_template('register.html', form=form)

configure_routes(app)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)