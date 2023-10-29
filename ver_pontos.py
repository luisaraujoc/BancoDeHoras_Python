from app import calcularHorasTotaisNoMes, dados


import PySimpleGUI as sg


def ver_pontos(matricula, mes):
    for funcionario in dados["funcionarios"]:
        if funcionario["matricula"] == matricula:
            if mes:
                # Calcular as horas totais no mês especificado
                horas_totais = calcularHorasTotaisNoMes(funcionario["pontos"], mes)
                sg.popup(f"Pontos de {funcionario['nome']} no mês {mes}:\nHoras trabalhadas no mês: {int(horas_totais)} horas {int((horas_totais - int(horas_totais)) * 60)} minutos")
            else:
                sg.popup("Por favor, insira o mês para gerar o relatório.")
            break
    else:
        sg.popup("Funcionário não encontrado.")