import tkinter as tk
from tkinter import messagebox

def agendamento_salaodebeleza(servicos):
    servicos.sort(key=lambda x: x[1])  # Ordena os serviços pelo horário de término
    n = len(servicos)
    memo = [0] * (n+1)

    for i in range(1, n+1):
        valor = servicos[i-1][2]
        j = i - 1
        while j >= 1 and servicos[j-1][1] > servicos[i-1][0]:
            j -= 1
        valor += memo[j]
        memo[i] = max(valor, memo[i-1])

    agendados = []
    i = n
    while i > 0:
        while i > 1 and memo[i] == memo[i-1]:
            i -= 1
        agendados.append(servicos[i-1])
        i -= 1
    agendados.reverse()

    return agendados

def agendar():
    servicos = []
    try:
        for i in range(len(entry_nomes)):
            nome = entry_nomes[i].get()
            inicio = int(entry_horarios_inicio[i].get())
            fim = int(entry_horarios_fim[i].get())
            valor = float(entry_valor[i].get())
            servicos.append((inicio, fim, valor, nome))

        agendados = agendamento_salaodebeleza(servicos)

        for widget in frame_agenda.winfo_children():
            widget.destroy()

        for i, (inicio, fim, valor, nome) in enumerate(agendados):
            label_cliente = tk.Label(frame_agenda, text=f"Cliente {i+1}: {inicio}h - {fim}h - Valor: R$ {valor:.2f} - Nome: {nome}")
            label_cliente.pack()

    except ValueError:
        messagebox.showerror("Erro", "Digite valores válidos para os horários e valor.")

root = tk.Tk()
root.title("Sistema de Agendamento de Salão de Beleza")
root.geometry("1000x700")

frame_inputs = tk.Frame(root)
frame_inputs.pack(padx=20, pady=20, expand=True, fill="both", anchor="center")

entry_num_clientes = tk.Entry(frame_inputs)
entry_num_clientes.grid(row=1, column=1, padx=10, pady=10, sticky="w")

entry_nomes = []
entry_horarios_inicio = []
entry_horarios_fim = []
entry_valor = []

def criar_campos_entrada():
    try:
        num_clientes = int(entry_num_clientes.get())
    except ValueError:
        messagebox.showerror("Erro", "Digite um valor válido para o número de clientes.")
        return

    for widget in frame_inputs.winfo_children():
        widget.destroy()

    label_nome = tk.Label(frame_inputs, text="Nome do cliente:")
    label_nome.grid(row=2, column=1, padx=5, pady=5, sticky="e")

    label_inicio = tk.Label(frame_inputs, text="Início do serviço:")
    label_inicio.grid(row=2, column=2, padx=5, pady=5, sticky="e")

    label_fim = tk.Label(frame_inputs, text="Término do serviço:")
    label_fim.grid(row=2, column=3, padx=5, pady=5, sticky="e")

    label_valor = tk.Label(frame_inputs, text="Valor do serviço:")
    label_valor.grid(row=2, column=4, padx=5, pady=5, sticky="e")

    for i in range(num_clientes):
        label_nome = tk.Label(frame_inputs, text=f"Nome do cliente {i+1}:")
        label_nome.grid(row=i+3, column=1, sticky="e")

        entry_nome = tk.Entry(frame_inputs)
        entry_nome.grid(row=i+3, column=2, padx=5, pady=5)
        entry_nomes.append(entry_nome)

        label_inicio = tk.Label(frame_inputs, text=f"Início do serviço (cliente {i+1}):")
        label_inicio.grid(row=i+3, column=3, sticky="e")

        entry_inicio = tk.Entry(frame_inputs)
        entry_inicio.grid(row=i+3, column=4, padx=5, pady=5)
        entry_horarios_inicio.append(entry_inicio)

        label_fim = tk.Label(frame_inputs, text=f"Término do serviço (cliente {i+1}):")
        label_fim.grid(row=i+3, column=5, sticky="e")

        entry_fim = tk.Entry(frame_inputs)
        entry_fim.grid(row=i+3, column=6, padx=5, pady=5)
        entry_horarios_fim.append(entry_fim)

        label_valor = tk.Label(frame_inputs, text=f"Valor do serviço (cliente {i+1}):")
        label_valor.grid(row=i+3, column=7, sticky="e")

        entry_val = tk.Entry(frame_inputs)
        entry_val.grid(row=i+3, column=8, padx=5, pady=5)
        entry_valor.append(entry_val)

    # Botão para agendar os serviços
    btn_agendar = tk.Button(frame_inputs, text="Agendar", command=agendar)
    btn_agendar.grid(row=num_clientes+3, column=4, padx=5, pady=10, sticky="e")

# Botão para criar os campos de entrada
btn_criar_campos = tk.Button(frame_inputs, text="Criar Campos", command=criar_campos_entrada)
btn_criar_campos.grid(row=1, column=2, padx=5, pady=10, sticky="w")

# Frame para exibir os dados agendados
frame_agenda = tk.Frame(root)
frame_agenda.pack(padx=20, pady=20)

# Execução da janela principal
root.mainloop()
