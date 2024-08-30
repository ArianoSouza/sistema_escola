from flask import Flask,render_template,request,redirect,jsonify,flash
from server import mongoConect
from cryptography.fernet import Fernet
import jwt
import uuid
import base64
import datetime


app = Flask(__name__,template_folder='templates',static_folder='static')

key_string = '65d68596-e0b9-47a8-af9f-ebccc0a5'
key_bytes = key_string.encode(encoding='utf-8')
key_b64 = base64.b64encode(key_bytes)
fernet = Fernet(key_b64)

server = mongoConect()
server.conection()
server_db = server.get_mongo_db()
alunos = server_db.get_collection('Alunos')
profs = server_db.get_collection('Professores')
cadeiras = server_db.get_collection('Cadeiras')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/home/aluno/<string:id>', methods=['GET'])
def enter(id):
    byte_id = str(id).encode('utf-8')
    decr_id = fernet.decrypt(byte_id).decode()
    print(decr_id)
    user = alunos.find_one({'id': int(decr_id)})
    return render_template('home_aluno.html', user_name = user['Nome'])


@app.route('/home/prof/<string:id>', methods=['GET'])
def enter_prof(id):
    byte_id = str(id).encode('utf-8')
    decr_id = fernet.decrypt(byte_id).decode()
    print(decr_id)
    user = profs.find_one({'id': int(decr_id)})
    return render_template('home_professor.html', user_name = user['nome'], id=id)


@app.route('/home/prof/<string:id>/turmas', methods=['GET'])
def turmas_prof(id):
    
    byte_id = str(id).encode('utf-8')
    decr_id = fernet.decrypt(byte_id).decode()
    user = profs.find_one({'id': int(decr_id)})
    turmas_relacionadas = []
    turma_prof = cadeiras.find({'prof_resp': int(decr_id)})
    
    for turmas in turma_prof:
        turmas_relacionadas.append(turmas)
    
    print(turmas_relacionadas)
    return render_template('prof_turmas.html', user_name = user['nome'], id=id, turmas_relacionadas=turmas_relacionadas)


@app.route('/home/prof/<string:id>/turmas/<string:turma_id>', methods=['GET'])
def turmas_prof_id(id,turma_id):
    turma = []
    pesq= request.args.get('aluno')
    all_alunos = alunos.find()
    turma_atual = cadeiras.find_one({'id': turma_id})
    
    for notas in turma_atual['notas']:
        for aluno in all_alunos:
            if aluno['id'] == notas['aluno']:
                turma.append(aluno['Nome'])
                break          
    return render_template('turmas_info.html', id=id, turma=turma,pesq=pesq)



@app.route('/login', methods=['POST', 'GET'])
def do_login(): 
    matricula = request.form.get('matricula')
    senha = request.form.get('senha')
    
    user =  alunos.find_one({'matricula':f'{matricula}'})
    prof_user = profs.find_one({'matricula':f'{matricula}'})
    
    if user == None and prof_user == None:
        print('error: login')
    elif user != None:
        if senha == fernet.decrypt(user['senha']).decode():
            return redirect(f'/home/aluno/{fernet.encrypt(str(user['id']).encode()).decode()}')
        else:
            print(user['senha'])
            print(fernet.encrypt(senha.encode('utf-8')))
            print('error: senha')
            
    elif prof_user != None:
        if senha == fernet.decrypt(prof_user['senha']).decode():
            return redirect(f'/home/prof/{fernet.encrypt(str(prof_user['id']).encode()).decode()}')
        else:
            print(fernet.encrypt(senha.encode('utf-8')).decode())
            print('error: senha')
    return render_template('login.html')
    
    


app.run(host='localHost',port="5000",debug=True)