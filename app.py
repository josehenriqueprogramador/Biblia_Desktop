from flask import Flask, render_template, request, redirect, url_for, session
import json, os
from models import LIVROS_NOMES

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta'
DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
versoes = sorted([f.replace('.json','') for f in os.listdir(DATA_DIR) if f.endswith('.json')])

def versao_atual():
    return session.get('versao','nvi')

def carregar_biblia(versao):
    path = os.path.join(DATA_DIR,f'{versao}.json')
    if not os.path.exists(path): return []
    with open(path,'r',encoding='utf-8-sig') as f:
        return json.load(f)

@app.context_processor
def inject_globals():
    return dict(LIVROS_NOMES=LIVROS_NOMES, versao=versao_atual(), versoes=versoes)

@app.route('/')
def index(): return redirect(url_for('livros'))

@app.route('/trocar_versao')
def trocar_versao():
    nova = request.args.get('versao','nvi')
    if nova in versoes: session['versao'] = nova
    return redirect(url_for('livros'))

@app.route('/livros')
def livros():
    biblia = carregar_biblia(versao_atual())
    return render_template('livros.html', livros=biblia)

@app.route('/capitulos/<livro_abrev>')
def capitulos(livro_abrev):
    biblia = carregar_biblia(versao_atual())
    livro = next((l for l in biblia if l.get('abbrev')==livro_abrev), None)
    if not livro: return 'Livro não encontrado',404
    total = len(livro.get('chapters',[]))
    return render_template('capitulos.html', livro=livro,total=total)

@app.route('/versiculos/<livro_abrev>/<int:capitulo>')
def versiculos(livro_abrev,capitulo):
    biblia = carregar_biblia(versao_atual())
    livro = next((l for l in biblia if l.get('abbrev')==livro_abrev), None)
    if not livro: return 'Livro não encontrado',404
    chapters = livro.get('chapters',[])
    if capitulo<1 or capitulo>len(chapters): return 'Capítulo não encontrado',404
    versiculos = chapters[capitulo-1]
    return render_template('versiculos.html', livro=livro,capitulo=capitulo,versiculos=versiculos)

if __name__=='__main__':
    app.run(host='0.0.0.0',port=5000,debug=True)
