from flask import Flask, render_template, request, redirect, url_for, flash
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, FileField, SubmitField
from wtforms.validators import DataRequired, URL
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your_secret_key')  # Use variável de ambiente
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

# Verifica se a extensão do arquivo é permitida
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# Formulário para a landing page
class LandingPageForm(FlaskForm):
    title = StringField('Título', validators=[DataRequired()])
    content = TextAreaField('Conteúdo', validators=[DataRequired()])
    images = FileField('Imagens', validators=[DataRequired()])
    url = StringField('URL', validators=[URL(message="URL inválida!"), DataRequired()])
    submit = SubmitField('Gerar Landing Page')

@app.route('/', methods=['GET', 'POST'])
def index():
    form = LandingPageForm()
    file_names = []

    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        
        # Manipulação do arquivo de imagem
        uploaded_files = request.files.getlist('images')  
        
        # Criação de diretório se não existir
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

        for file in uploaded_files:
            if allowed_file(file.filename):
                filename = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file.filename))
                file.save(filename)
                file_names.append(file.filename)
            else:
                flash(f'Tipo de arquivo não permitido: {file.filename}', 'danger')
                return redirect(request.url)

        flash('Landing Page gerada com sucesso!', 'success')
        return render_template('landing_page.html', title=title, content=content, images=file_names)

    return render_template('index.html', form=form)

@app.route('/landing_page')
def landing_page():
    return render_template('landing_page.html')

# Endpoint para deletar imagens
@app.route('/delete_image/<filename>', methods=['POST'])
def delete_image(filename):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if os.path.exists(file_path):
        os.remove(file_path)
        flash(f'Imagem {filename} removida com sucesso.', 'success')
    else:
        flash(f'Imagem {filename} não encontrada.', 'danger')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)