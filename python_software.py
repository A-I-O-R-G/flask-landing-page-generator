from flask import Flask, render_template, request, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, FileField, SubmitField
from wtforms.validators import DataRequired
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

# Verifica se a extensão do arquivo é permitida
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# Formulário para a landing page
class LandingPageForm(FlaskForm):
    title = StringField('Título', validators=[DataRequired()])
    content = TextAreaField('Conteúdo', validators=[DataRequired()])
    image = FileField('Imagem')
    submit = SubmitField('Gerar Landing Page')

@app.route('/', methods=['GET', 'POST'])
def index():
    form = LandingPageForm()
    
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        
        # Manipulação do arquivo de imagem
        if form.image.data:
            file = form.image.data
            if allowed_file(file.filename):
                filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
                file.save(filename)
            else:
                return 'Tipo de arquivo não permitido', 400
                
        # Renderiza a landing page com os dados fornecidos
        return render_template('landing_page.html', title=title, content=content, image=file.filename)

    return render_template('index.html', form=form)

@app.route('/landing_page')
def landing_page():
    return render_template('landing_page.html')

if __name__ == '__main__':
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    app.run(debug=True)