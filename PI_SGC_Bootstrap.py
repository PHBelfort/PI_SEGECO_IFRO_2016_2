import os
import pymysql
from flask import Flask, request, redirect, session, flash, jsonify
from flask.helpers import url_for
from flask import render_template

app = Flask(__name__)

# conexão mysql
conexao = pymysql.connect(
    host='localhost',
    user='root',
    passwd='1234',
    db='segeco'
)
conexao_cursor = conexao.cursor()

@app.route('/')
@app.route('/index')
def retorna_index():
    return render_template('index.html')


@app.route('/acessar', methods=['GET', 'POST'])
def acessar():
    return render_template('acessar.html')

@app.route('/login', methods=['GET', 'POST'])
def acessar_admin():
    error = None

    if request.method == 'POST':
        usu_nome = request.form['cpf']
        usu_senha = request.form['senha']

        # Valida o formulario de login
        if usu_nome == '' or usu_senha == '':
            error = 'Os campos  Nome e Senha são obrigatorios.!'

        else:
            codigo_sql = """
                        SELECT * FROM usuario WHERE cpf = '{}' AND senha = '{}'
                        """.format(usu_nome, usu_senha)
            #return jsonify(codigo_sql)
            conexao_cursor.execute(codigo_sql)
            existe_user = conexao_cursor.fetchall()

            return jsonify(existe_user)

            # Se o usuario existir conecta com sucesso
            if existe_user:
                # Adiciona os valores na session
                session['nome'] = request.form['nome']
                session['codigo'] = existe_user[0][0]
                session['cargo'] = existe_user[0][3]

                flash('Conectado com sucesso')
                return redirect(url_for('admin/ger_certificados'))

            # Se não existir retorna uma mensagem de erro
            if not existe_user:
                error = 'O usuario e/ou senha não existe. Por favor, contate o administrador.!'

    return render_template('ger_certificados', error=error)


@app.route('/logado_sessao/', methods=['GET', 'POST'])
def logado_sessao():

    # para saber se o usuário e a senha foram inseridos corretamente
    # verificamos se existe o usuário na sessão
    if 'cpf' in session:
        return render_template('admin/ger_certificados.html')


@app.route('/encerrar_sessao')
def encerrar_sessao():
    # remove o usuário logado da sessão atual
    session.pop('cpf', None)
    return redirect(url_for('acessar'))



@app.route('/ger_certificados')
def ger_certificados():
    # monta o select para pegar todos os registros
    codigo_sql = """
                    SELECT * FROM certificado
                """

    # executa o código sql
    conexao_cursor.execute(codigo_sql)
    # salva em contatos todos os consultados no banco
    certificado = conexao_cursor.fetchall()

    # exibe todos os registros no template
    return render_template('admin/ger_certificados.html', certificados=certificado)


@app.route('/admin_cert_do_usuario')
def admin_cert_do_usuario():
    # monta o select para pegar todos os registros
    codigo_sql = """
                    SELECT * FROM certificado
                """

    # executa o código sql
    conexao_cursor.execute(codigo_sql)
    # salva em contatos todos os consultados no banco
    certificado = conexao_cursor.fetchall()

    # exibe todos os registros no template
    return render_template('admin/admin_cert_do_usuario.html', certificados=certificado)


@app.route('/cadastrar_certificado', methods=['GET', 'POST'])
def cadastrar_certificado():
    if request.method == 'POST':
        # pega os dados do formulário via request
        plano_fundo = request.form['plano_fundo']
        texto_antes_nome = request.form['texto_antes_nome']
        texto_pos_nome = request.form['texto_pos_nome']
        # monta o sql para atualizar
        codigo_sql = """
            INSERT INTO layout_certificados (plano_fundo, texto_antes_nome, texto_pos_nome)
            VALUES ('{}', '{}', '{}')
        """.format(plano_fundo, texto_antes_nome, texto_pos_nome)

        conexao_cursor.execute(codigo_sql)  # executa no banco
        conexao.commit()  # salva a alteração

    return render_template('admin/cadastrar_certificado.html')

@app.route('/ger_usuarios', methods=['GET', 'POST'])
def retorna_ger_usuarios():
    # monta o select para pegar todos os registros
    codigo_sql = """
            SELECT * FROM usuario
        """

    # executa o código sql
    conexao_cursor.execute(codigo_sql)
    # salva em contatos todos os consultados no banco
    cadastro = conexao_cursor.fetchall()

    # exibe todos os registros no template
    return render_template('admin/ger_usuarios.html', cadastro=cadastro)


def excluir_ger_usuarios(nome):

    # se clicou no botão "excluir"
    # monta o código sql para excluir se for o ID tal...
    codigo_sql = "DELETE FROM usuario WHERE nome={}".format('nome')

    conexao_cursor.execute(codigo_sql)  # executa no banco

    # redireciona para a página com todos os contatos
    return  render_template('admin/ger_usuarios.html')


@app.route('/visualizar_cadastro_usuario', methods=['GET'])
def retorna_view():
    # monta o select para pegar todos os registros
    codigo_sql = """
                SELECT * FROM usuario
            """

    # executa o código sql
    conexao_cursor.execute(codigo_sql)
    # salva em contatos todos os consultados no banco
    cadastro = conexao_cursor.fetchall()

    # exibe todos os registros no template
    return render_template('admin/visualizar_cadastro_usuario.html', cadastrados=cadastro)


@app.route('/view_certificado', methods=['GET'])
def layouts_certificado():
    # monta o select para pegar todos os registros
    codigo_sql = """
                SELECT * FROM layout_certificados
            """

    # executa o código sql
    conexao_cursor.execute(codigo_sql)
    # salva em contatos todos os consultados no banco
    layout = conexao_cursor.fetchall()

    # exibe todos os registros no template
    return render_template('admin/view_certificado.html', layouts=layout)


@app.route('/add_usuario', methods=['GET', 'POST'])
def add_usuario():
    if request.method == 'POST':
        # pega os dados do formulário via request
        cpf = request.form['cpf']
        nome = request.form['nome']
        data_nascimento = request.form['data_nascimento']
        data2 = data_nascimento.split('/')
        data_nascimento = '{}-{}-{}'.format(data2[2],data2[1],data2[0])
        sexo = request.form['sexo']
        email = request.form['email']
        n_celular = request.form['n_celular']
        tel_fixo = request.form['tel_fixo']
        campus_polo = request.form['campus_polo']
        curso_departamento = request.form['curso_departamento']
        senha = request.form['senha']
        conf_senha = request.form['conf_senha']

        # monta o sql para atualizar
        codigo_sql = """
            INSERT INTO usuario (cpf, nome, data_nascimento, sexo, email, n_celular, tel_fixo, campus_polo, curso_departamento, senha, conf_senha)
            VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')
        """.format(cpf, nome, data_nascimento, sexo, email, n_celular, tel_fixo, campus_polo, curso_departamento, senha, conf_senha)

        conexao_cursor.execute(codigo_sql)  # executa no banco
        conexao.commit()  # salva a alteração

        # redireciona para a página com todos os usuarios
        return redirect(url_for('ger_usuarios'))

    return render_template('add_usuario.html')


@app.route('/usuarios/editar/<int:id>', methods=['GET', 'POST'])
def editar_usuario(id):

    # se clicou no botão "atualizar"
    if request.method == 'POST':
        # pega os dados do formulário via request
        cpf = request.form['cpf']
        nome = request.form['nome']
        data_nascimento = request.form['data_nascimento']
        data2 = data_nascimento.split('/')
        data_nascimento = '{}-{}-{}'.format(data2[2], data2[1], data2[0])
        sexo = request.form['sexo']
        email = request.form['email']
        n_celular = request.form['n_celular']
        tel_fixo = request.form['tel_fixo']
        campus_polo = request.form['campus_polo']
        curso_departamento = request.form['curso_departamento']
        senha = request.form['senha']
        conf_senha = request.form['conf_senha']

        # monta o sql para atualizar
        codigo_sql = """
            UPDATE usuario
            SET cpf='{}', nome='{}', data_nascimento='{}', sexo='{}', email='{}', n_celular='{}', tel_fixo='{}', campus_polo='{}', curso_departamento='{}', senha='{}', conf_senha='{}'
            WHERE id='{}'
        """.format(cpf, nome, data_nascimento, sexo, email, n_celular, tel_fixo, campus_polo, curso_departamento, senha, conf_senha)

        conexao_cursor.execute(codigo_sql)  # executa no banco
        conexao.commit()  # salva a alteração

        # redireciona para a página com todos os contatos
        return redirect(url_for('ger_usuarios.html'))

    # se não foi um post então consulta e mostra na página
    # monta o sql para consultar o registro pelo id
    codigo_sql = "SELECT * FROM usuario WHERE id = {}".format(id)

    # executa o código sql
    conexao_cursor.execute(codigo_sql)
    # salva em contato todos os consultados no banco
    nome = conexao_cursor.fetchall()

    # mostra no template o contato[0], pois vem como uma lista contento 1 elemento apenas
    return render_template('admin/editar_usuario.html', nome=nome[0])


@app.route('/user_view')
def retorna_user_view():
    return render_template('usuario/user_view.html')

@app.route('/tela_user')
def retorna_tela_user():
    # monta o select para pegar todos os registros
    codigo_sql = """
                    SELECT * FROM certificado
                """

    # executa o código sql
    conexao_cursor.execute(codigo_sql)
    # salva em contatos todos os consultados no banco
    certificado = conexao_cursor.fetchall()

    # exibe todos os registros no template
    return render_template('usuario/tela_user.html', certificados=certificado)


@app.route('/user_cadastro', methods=['GET', 'POST'])
def user_cadastro():
    # monta o select para pegar todos os registros
    codigo_sql = """
                SELECT * FROM usuario
            """

    # executa o código sql
    conexao_cursor.execute(codigo_sql)
    # salva em contatos todos os consultados no banco
    cadastro = conexao_cursor.fetchall()

    # exibe todos os registros no template
    return render_template('usuario/user_cadastro.html', cadastrados=cadastro)


@app.route('/cadastro', methods=['GET', 'POST'])
def criar_cadastro():
    if request.method == 'POST':
        # pega os dados do formulário via request
        cpf = request.form['cpf']
        nome = request.form['nome']
        data_nascimento = request.form['data_nascimento']
        data2 = data_nascimento.split('/')
        data_nascimento = '{}-{}-{}'.format(data2[2],data2[1],data2[0])
        sexo = request.form['sexo']
        email = request.form['email']
        n_celular = request.form['n_celular']
        tel_fixo = request.form['tel_fixo']
        campus_polo = request.form['campus_polo']
        curso_departamento = request.form['curso_departamento']
        senha = request.form['senha']
        conf_senha = request.form['conf_senha']

        # monta o sql para atualizar
        codigo_sql = """
            INSERT INTO usuario (cpf, nome, data_nascimento, sexo, email, n_celular, tel_fixo, campus_polo, curso_departamento, senha, conf_senha)
            VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')
        """.format(cpf, nome, data_nascimento, sexo, email, n_celular, tel_fixo, campus_polo, curso_departamento, senha, conf_senha)

        conexao_cursor.execute(codigo_sql)  # executa no banco
        conexao.commit()  # salva a alteração

    return render_template('cadastro.html')

@app.route('/cadastrar_evento', methods=['GET', 'POST'])
def cadastrar_evento():
    if request.method == 'POST':
        # pega os dados do formulário via request
        nome_evento = request.form['nome_evento']
        data_realizacao = request.form['data_realizacao']
        carga_horaria = request.form['carga_horaria']
        local_evento = request.form['local_evento']
        responsavel = request.form['responsavel']
        layout_certificados = request.form['layout_certificados']
        # monta o sql para atualizar
        codigo_sql = """
            INSERT INTO eventos (nome_evento, data_realizacao, carga_horaria, local_evento, responsavel, layout_certificados)
            VALUES ('{}', '{}', '{}', '{}', '{}', '{}')
        """.format(nome_evento, data_realizacao, carga_horaria, local_evento, responsavel, layout_certificados)

        conexao_cursor.execute(codigo_sql)  # executa no banco
        conexao.commit()  # salva a alteração

    return render_template('admin/cadastrar_evento.html')

@app.route('/eventos_view')
def retorna_eventos_view():
    # monta o select para pegar todos os registros
    codigo_sql = """
                    SELECT * FROM eventos
                """

    # executa o código sql
    conexao_cursor.execute(codigo_sql)
    # salva em contatos todos os consultados no banco
    evento = conexao_cursor.fetchall()

    # exibe todos os registros no template
    return render_template('admin/eventos_view.html', eventos_cad = evento)

@app.route('/validar_certificado')
def retorna_validar_certificado():
    return render_template('validar_certificado.html')

@app.route('/sobre')
def retorna_sobre():
    return render_template('sobre.html')


if __name__ == '__main__':
    # inclua essas linhas para pegar a porta e o ip configurados no heroku ou c9 por exemplo
    porta = int(os.getenv('PORT', 5000))
    host = os.getenv('IP', 'localhost')
    # lembre-se sempre de ativar o debug para visualizar melhor
    # os erros e reiniciar automaticamente seu servidor
    app.run(debug=True, port=porta, host=host)
