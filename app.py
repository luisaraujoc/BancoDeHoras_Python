import json
import datetime
import PySimpleGUI as sg

from dracula_theme import dracula_theme

## Para conhecimento

# Estrutura de dados em Python para representar o JSON
estrutura_pontos = {
    "funcionarios": [
        {
            "matricula": "12345",
            "nome": "Exemplo1",
            "pontos": [
                {"data": "01-01-2023", "hora": "08:00"},
                {"data": "01-01-2023", "hora": "12:00"},
                {"data": "01-01-2023", "hora": "13:00"},
                {"data": "01-01-2023", "hora": "17:00"},
                {"data": "02-01-2023", "hora": "08:30"},
                {"data": "02-01-2023", "hora": "16:30"},
            ]
        },
        {
            "matricula": "54321",
            "nome": "Exemplo2",
            "pontos": [
                {"data": "01-01-2023", "hora": "09:00"},
                {"data": "01-01-2023", "hora": "12:30"},
                {"data": "01-01-2023", "hora": "14:00"},
                {"data": "01-01-2023", "hora": "18:30"},
            ]
        }
    ]
}

# Código em si

dataHoraAtual = datetime.datetime.now()


# Defina o tema como 'Dracula'
sg.theme('Dracula')


layout = [
    [sg.Text("Matrícula do Funcionário:"), sg.InputText(key="matricula")],
    [sg.Text("Nome do Funcionário:"), sg.InputText(key="nome")],
    [sg.Button("Registrar Ponto"), sg.Button("Registrar Funcionário"), sg.Button("Sair")],
    [sg.Text("", size=(40, 1), key="output")],
    [sg.Text("Ver Pontos do Funcionário:")],
    [sg.Text("Data dos pontos:"), sg.InputText(key="matricula_ver_pontos")],
    [sg.Text("Data dos pontos:"), sg.InputText(default_text=dataHoraAtual.strftime("%d-%m-%Y"), key="data_ver_pontos")],
    [sg.Button("Ver")],
    # [sg.Multiline("", size=(40, 6), key="pontos_registrados")],
]

window = sg.Window("Controle de Ponto", layout)

# Dicionário para rastrear se o campo perdeu o foco
focus_lost = {
    "matricula": False,
    "nome": False,
    "matricula_ver_pontos": False,
    "data_ver_pontos": False
}

# Função para carregar os dados do arquivo JSON
def carregarDados(nomeArquivo):
    try:
        with open(nomeArquivo, 'r') as arquivo:
            dados = json.load(arquivo)
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        dados = {"funcionarios": []}
    return dados

# Função para salvar os dados no arquivo JSON
def salvarDados(nomeArquivo, dados):
    with open(nomeArquivo, 'w') as arquivo:
        json.dump(dados, arquivo, indent=4)

# Função para registrar o ponto de um funcionário usando a matrícula
def registrarPontoPorMatricula(dados, matricula):
    funcionarios = dados.get("funcionarios", [])
    for funcionario in funcionarios:
        if funcionario["matricula"] == matricula:
            if len(funcionario["pontos"]) < 6:
                dataHoraAtual = datetime.datetime.now()
                data = dataHoraAtual.strftime("%d-%m-%Y")
                hora = dataHoraAtual.strftime("%H:%M")
                novoPonto = {"data": data, "hora": hora}
                funcionario["pontos"].append(novoPonto)
                if len(funcionario["pontos"]) == 6:
                    print("Atenção: Você atingiu o máximo de 6 pontos registrados.")
                    break

# Função para adicionar um novo funcionário
def adicionarFuncionario(dados, matricula, nome):
    funcionarios = dados.get("funcionarios", [])
    novoFuncionario = {
        "matricula": matricula,
        "nome": nome,
        "pontos": []
    }
    funcionarios.append(novoFuncionario)
    dados["funcionarios"] = funcionarios

# Função para calcular a quantidade de horas trabalhadas em um dia
def calcularHorasTrabalhadas(pontos):
    if len(pontos) <= 6:
        # return 0
        horas_entrada = [ponto["hora"] for i, ponto in enumerate(pontos) if i % 2 == 0]
        horas_saida = [ponto["hora"] for i, ponto in enumerate(pontos) if i % 2 == 1]
        horas_trabalhadas = sum([calcularDiferencaHoras(entrada, saida) for entrada, saida in zip(horas_entrada, horas_saida)])
    return horas_trabalhadas

# Função para calcular a diferença entre duas horas no formato HH:MM
def calcularDiferencaHoras(hora1, hora2):
    h1, m1 = map(int, hora1.split(":"))
    h2, m2 = map(int, hora2.split(":"))
    return (h2 - h1) + (m2 - m1) / 60

def registrar_ponto(matricula):
    # Chamada para a função registrarPontoPorMatricula com a matrícula fornecida
    registrarPontoPorMatricula(dados, matricula)
    salvarDados(nomeArquivo, dados)
    sg.popup("Ponto registrado com sucesso.")

# Função para adicionar um novo funcionário quando o botão for pressionado
def adicionar_funcionario(matricula, nome):
    # Chamada para a função adicionarFuncionario com a matrícula e nome fornecidos
    adicionarFuncionario(dados, matricula, nome)
    salvarDados(nomeArquivo, dados)
    sg.popup("Funcionário registrado com sucesso.")
    
def ver_pontos(matricula, data):
    for funcionario in dados["funcionarios"]:
        if funcionario["matricula"] == matricula:
            pontos_funcionario = [ponto for ponto in funcionario["pontos"] if ponto["data"] == data]
            if pontos_funcionario:
                horas_trabalhadas = calcularHorasTrabalhadas(pontos_funcionario)
                pontos_text = "\n".join(f"{ponto['hora']}" for ponto in pontos_funcionario)
                sg.popup(f"Pontos de {funcionario['nome']} em {data}:\n{pontos_text}\nHoras trabalhadas: {int(horas_trabalhadas)} horas {int((horas_trabalhadas - int(horas_trabalhadas)) * 60)} minutos")
                break
            else:
                sg.popup(f"Nenhum ponto registrado para {funcionario['nome']} em {data}")
    else:
        sg.popup("Funcionário não encontrado.")

# Exemplo de uso
nomeArquivo = "controlePonto.json"
dados = carregarDados(nomeArquivo)

# Loop principal da interface gráfica
while True:
    event, values = window.read()

    if event == sg.WINDOW_CLOSED or event == "Sair":
        break
    elif event == "Registrar Ponto":
        matricula = values["matricula"]
        if matricula:
            registrar_ponto(matricula)
        else:
            sg.popup("Por favor, insira a matrícula.")
    elif event == "Registrar Funcionário":
        matricula = values["matricula"]
        nome = values["nome"]
        if matricula and nome:
            adicionar_funcionario(matricula, nome)
        else:
            sg.popup("Por favor, insira a matrícula e o nome.")
    elif event == "Ver":
        matricula_ver_pontos = values["matricula_ver_pontos"]
        data_ver_pontos = values["data_ver_pontos"]
        if matricula_ver_pontos and data_ver_pontos:
            ver_pontos(matricula_ver_pontos, data_ver_pontos)
        else:
            sg.popup("Por favor, insira a matrícula e a data.")

    # Lidar com o evento FocusIn para remover o texto de placeholder
    for key in focus_lost:
        if event == f"{key}_FOCUSIN":
            if values[key] == f"Insira {key}":
                window[key]("")
                focus_lost[key] = True

    # Lidar com o evento FocusOut para reverter para o texto de placeholder, se necessário
    for key in focus_lost:
        if event == f"{key}_FOCUSOUT" and not values[key]:
            window[key](f"Insira {key}")

window.close()