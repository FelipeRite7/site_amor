from flask import Flask, render_template, request, redirect, session, flash

app = Flask(__name__)
app.secret_key = '45949867'

class Palavra:
    def __init__(self, elogio, qualidade, pessoa):
        self.elogio = elogio
        self.qualidade = qualidade
        self.pessoa = pessoa

palavra1 = Palavra('Perfeita', 'Se preocupa com quem ama', 'coração bom demais')
palavra2 = Palavra('Deusa', 'esforçada mesmo com problemas', 'inteligentissima')
palavra3 = Palavra('Zero defeitos', 'Sua força é enorme', 'Minha MULHER')

palavras = [palavra1, palavra2, palavra3]

class Usuario:
    def __init__(self, usuario, nickname, senha):
        self.usuario = usuario
        self.senha = senha
        self.nickname = nickname

usuario1 = Usuario("Ana Scodeler", "Perfeita", "matheus2511")
usuario2 = Usuario("Felipe Rite", "lindo", "45949867")

usuarios = {usuario1.nickname: usuario1,
            usuario2.nickname: usuario2}

@app.route("/", methods=['GET', 'POST'])
def pagina_inicial():
    if 'usuario_logado' not in session or session['usuario_logado'] is None:
        return redirect('/login')
    else:
        if request.method == 'POST':
            option = request.form.get('option')
            if option == 'opcao1':
                frase = 'Meu amor, nada neste mundo me faz mais feliz do que estar na sua companhia.'
            elif option == 'opcao2':
                frase = 'Quem carrega sempre um sorriso no rosto sou eu, mas a razão é você, meu amor.'
            elif option == 'opcao3':
                frase = 'Minha princesa, minha guerreira, minha companheira de aventuras: minha namorada.'
            elif option == 'opcao4':
                frase = 'Você é o maior e melhor presente que Deus já me concedeu.'
            else:
                frase = 'Opção inválida.'

            return render_template('pagina_inicial.html', frase=frase, palavras=palavras)

        return render_template("pagina_inicial.html")

@app.route('/declaracao', methods=['GET', 'POST'])
def declaracao():
    if 'usuario_logado' not in session or session['usuario_logado'] is None:
        return redirect('/login')

    if request.method == 'POST':
        elogio = request.form['elogio']
        qualidade = request.form['qualidade']
        texto_declaracao = request.form['texto_declaracao']  # Alteração feita aqui
        nova_palavra = Palavra(elogio, qualidade, texto_declaracao)  # Alteração feita aqui
        palavras.append(nova_palavra)
        return redirect('/')
    else:
        return render_template('novo.html')


@app.route('/lista')
def lista_declaracoes():
    return render_template('lista.html', palavras=palavras)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'usuario_logado' in session and session['usuario_logado'] is not None:
        return redirect('/')

    if request.method == 'POST':
        usuario = request.form['usuario']
        senha = request.form['senha']

        if usuario in usuarios and usuarios[usuario].senha == senha:
            session['usuario_logado'] = usuario
            flash(usuario + ' logado com sucesso!')
            return redirect('/')
        else:
            flash('Usuário não logado!')
            return redirect('/login')

    return render_template('login.html')

@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    flash('Logout efetuado com sucesso!')
    return redirect('/login')

if __name__ == "__main__":
    app.run(debug=True)