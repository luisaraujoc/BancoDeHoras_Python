import json
import datetime
import PySimpleGUI as sg
from dracula_theme import dracula_theme
from ver_pontos import ver_pontos

# Código em si

dataHoraAtual = datetime.datetime.now()

# Defina o tema como 'DarkGrey5'

sg.theme_add_new('Dracula', dracula_theme)
sg.theme('Dracula')

layout = [
    [sg.Text("Matrícula do Funcionário:"), sg.InputText(key="matricula")],
    [sg.Text("Nome do Funcionário:"), sg.InputText(key="nome")],  # Adicione o campo de nome
    [sg.Button("Registrar Ponto"), sg.Button("Registrar Funcionário"), sg.Button("Sair")],
    [sg.Text("", size=(40, 1), key="output")],
    [sg.Text("Ver Pontos do Funcionário:")],
    [sg.Text("Matrícula do funcionário:"), sg.InputText(key="matricula_ver_pontos")],
    [sg.Text("Mês dos pontos:"), sg.InputText(default_text=dataHoraAtual.strftime("%m-%Y"), key="mes_ver_pontos")],  # Adicione o campo de mês
    [sg.Button("Ver")],
]

window = sg.Window("Controle de Ponto", layout)

# Dicionário para rastrear se o campo perdeu o foco
focus_lost = {
    "matricula": False,
    "nome": False,
    "matricula_ver_pontos": False,
    "mes_ver_pontos": False  # Adicione o campo de mês
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
def salvarFuncionário(dados, matricula, nome):
    funcionarios = dados.get("funcionarios", [])
    for funcionario in funcionarios:
        if funcionario["matricula"] == matricula:
            funcionario["nome"] = nome
            break
    else:
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

# Função para calcular as horas totais no mês
def calcularHorasTotaisNoMes(pontos, mes):
    horas_totais = 0
    for ponto in pontos:
        if ponto["data"].endswith(mes):
            horas_totais += calcularHorasTrabalhadas([p for p in pontos if p["data"].endswith(mes)])
    return horas_totais

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

# Modifique a função adicionar_funcionario para permitir atualização
def adicionar_funcionario(matricula, nome):
    # Chamada para a função salvarFuncionário com a matrícula e nome fornecidos
    salvarFuncionário(dados, matricula, nome)
    salvarDados(nomeArquivo, dados)
    sg.popup("Funcionário registrado/atualizado com sucesso.")

# Modifique a função ver_pontos para permitir a escolha do mês para o relatório
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
        mes_ver_pontos = values["mes_ver_pontos"]
        if matricula_ver_pontos and mes_ver_pontos:
            ver_pontos(matricula_ver_pontos, mes_ver_pontos)
        else:
            sg.popup("Por favor, insira a matrícula e o mês.")

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
