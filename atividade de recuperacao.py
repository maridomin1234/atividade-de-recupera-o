import sqlite3
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk


# Conectar ao banco de dados SQLite
def conectar_bd():
    conn = sqlite3.connect('times_volei.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS times (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        nome TEXT NOT NULL,
                        cidade TEXT NOT NULL,
                        treinador TEXT NOT NULL)''')
    conn.commit()
    return conn


# Função para inserir um time
def inserir_time():
    nome = entry_nome.get()
    cidade = entry_cidade.get()
    treinador = entry_treinador.get()

    if nome and cidade and treinador:
        conn = conectar_bd()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO times (nome, cidade, treinador) VALUES (?, ?, ?)", (nome, cidade, treinador))
        conn.commit()
        conn.close()
        exibir_times()
        limpar_campos()
    else:
        messagebox.showwarning("Erro", "Todos os campos são obrigatórios.")


# Função para atualizar um time
def atualizar_time():
    try:
        id_time = tree.selection()[0]
        nome = entry_nome.get()
        cidade = entry_cidade.get()
        treinador = entry_treinador.get()

        if nome and cidade and treinador:
            conn = conectar_bd()
            cursor = conn.cursor()
            cursor.execute("UPDATE times SET nome = ?, cidade = ?, treinador = ? WHERE id = ?",
                           (nome, cidade, treinador, id_time))
            conn.commit()
            conn.close()
            exibir_times()
            limpar_campos()
        else:
            messagebox.showwarning("Erro", "Todos os campos são obrigatórios.")
    except IndexError:
        messagebox.showwarning("Erro", "Selecione um time para atualizar.")


# Função para excluir um time
def excluir_time():
    try:
        id_time = tree.selection()[0]
        conn = conectar_bd()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM times WHERE id = ?", (id_time,))
        conn.commit()
        conn.close()
        exibir_times()
        limpar_campos()
    except IndexError:
        messagebox.showwarning("Erro", "Selecione um time para excluir.")


# Função para exibir os times na tabela
def exibir_times():
    for row in tree.get_children():
        tree.delete(row)

    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM times")
    rows = cursor.fetchall()
    for row in rows:
        tree.insert("", tk.END, row[0], values=(row[1], row[2], row[3]))
    conn.close()


# Função para limpar os campos
def limpar_campos():
    entry_nome.delete(0, tk.END)
    entry_cidade.delete(0, tk.END)
    entry_treinador.delete(0, tk.END)


# Interface gráfica com Tkinter
app = tk.Tk()
app.title("Gestão de Times de Vôlei")

# Labels e entradas
tk.Label(app, text="Nome do Time:").grid(row=0, column=0, padx=10, pady=10)
entry_nome = tk.Entry(app)
entry_nome.grid(row=0, column=1, padx=10, pady=10)

tk.Label(app, text="Cidade:").grid(row=1, column=0, padx=10, pady=10)
entry_cidade = tk.Entry(app)
entry_cidade.grid(row=1, column=1, padx=10, pady=10)

tk.Label(app, text="Treinador:").grid(row=2, column=0, padx=10, pady=10)
entry_treinador = tk.Entry(app)
entry_treinador.grid(row=2, column=1, padx=10, pady=10)

# Botões
btn_inserir = tk.Button(app, text="Inserir Time", command=inserir_time)
btn_inserir.grid(row=3, column=0, padx=10, pady=10)

btn_atualizar = tk.Button(app, text="Atualizar Time", command=atualizar_time)
btn_atualizar.grid(row=3, column=1, padx=10, pady=10)

btn_excluir = tk.Button(app, text="Excluir Time", command=excluir_time)
btn_excluir.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

# Tabela para exibir os times
tree = ttk.Treeview(app, columns=("nome", "cidade", "treinador"), show="headings")
tree.heading("nome", text="Nome")
tree.heading("cidade", text="Cidade")
tree.heading("treinador", text="Treinador")
tree.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

# Exibir os times ao iniciar
exibir_times()

app.mainloop()