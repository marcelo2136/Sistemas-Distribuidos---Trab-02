from flask import Flask, jsonify, request

class Apicultor:
    def __init__(self, nome, idade):
        self.nome = nome
        self.idade = idade
        
    def str_apicultor(self):
        return "Nome: " + self.nome + " | Idade: " + str(self.idade)


class Apiario:
    def __init__(self, id, num_colmeias):
        self.id = id
        self.num_colmeias = num_colmeias
        self.apicultores = []

    def str_apiario(self):
        strg = ""
        strg += "Apiario " + str(self.id) + " com " + str(self.num_colmeias) + " colmeias"
        return strg

    def get_apic_numb(self):
        return len(self.apicultores)

    def get_apicultor(self, id):
        return self.apicultores[id].str_apicultor()

    def add_apicultores(self, apicultor):
        self.apicultores.append(apicultor)

    def set_id(self, id):
        self.id = id


lista = []

# "Using" indica se é uma mensagem de comando ou um objeto/resposta. Caso for True, o programa não lerá input
# Comandos (para o servidor):
#   $A{numero} ->   (client) Adicionar objeto (numero = 1 (Apiario) ; numero = 2 (Apicultor))
#                   (server) Autorização para enviar objeto
#   $C{numero}{index} ->   (client) Consulta {numero = 0 (Apiario) ; numero = 1 (Todos os Apiarios)}
#                                            {index = posição do Apiario na lista}
#   #A1 -> Resposta do servidor, em texto.

app = Flask(__name__)

#GET obter todos os apiários e funcionários
@app.route('/apiario', methods=['GET'])
def consult_apiarios():
    new_list = {}
    for ap in lista:
        new_list[str(ap.id)] = ap.str_apiario()

        for numb in range(ap.get_apic_numb()):
            str_aux = ""
            str_aux += str(ap.id) + ', Funcionario ' + str(numb)
            new_list[str_aux] = ap.get_apicultor(numb)

    return jsonify(new_list)

#GET obter apiário específico
@app.route('/apiario/<int:id>', methods=['GET'])
def consult_apiarios_id(id):
    new_list = {}

    for ap in lista:
        if ap.id == id:
            new_list["Apiario"] = ap.str_apiario()

            for numb in range(ap.get_apic_numb()):
                str_aux = "Funcionario " + str(numb)
                new_list[str_aux] = ap.get_apicultor(numb)

    return jsonify(new_list)

#POST criar novo apiário
@app.route('/apiario', methods=['POST'])
def add_apiario():
    ap_data = request.get_json()
    novo_ap = Apiario(ap_data["id"], ap_data["num_colmeias"])
    lista.append(novo_ap)
    
    new_list = {}
    for ap in lista:
        new_list[str(ap.id)] = ap.str_apiario()
    return jsonify(new_list)

#POST criar apicultor específico
@app.route('/apiario/<int:id>', methods=['POST'])
def add_apicultor(id):
    ap_data = request.get_json()
    novo_ap = Apicultor(ap_data["nome"], ap_data["idade"])

    new_list = {}

    new_list["Nome"] = ap_data["nome"]
    new_list["Idade"] = ap_data["idade"]

    for ap in lista:
        if ap.id == id:
            ap.add_apicultores(novo_ap)

    return jsonify(new_list)

#DELETE apaga um apiário
@app.route('/apiario/<int:id>', methods=['DELETE'])
def delete_apiario(id):
    
    new_list = {}

    for ap in lista:
        if ap.id == id:
            lista.remove(ap)
    for ap in lista:
            new_list[str(ap.id)] = ap.str_apiario()

    return jsonify(new_list)

#DELETE apaga um apicultor
@app.route('/apiario/<int:id>/<int:id2>', methods=['DELETE'])
def delete_apicultor(id,id2):
    
    new_list = {}

    for ap in lista:
        if ap.id == id:
            del ap.apicultores[id2]
            new_list["Apiario"] = ap.str_apiario()

            for numb in range(ap.get_apic_numb()):
                str_aux = "Funcionario " + str(numb)
                new_list[str_aux] = ap.get_apicultor(numb)

    return jsonify(new_list)

app.run(port=5000,host='localhost',debug=True) 