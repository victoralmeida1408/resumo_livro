import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import google.generativeai as genai
from PIL import Image, ImageTk  # Para manipulação da imagem

# Configure sua chave Gemini (substitua pela sua chave válida do Google AI Studio)
genai.configure()

# Função para gerar resumo com Gemini
def obter_resumo(titulo_livro):
    prompt = f"""
    Você é um especialista literário. Gere um resumo detalhado e envolvente do livro chamado: "{titulo_livro}".
    Foque na narrativa principal, apresentando a premissa, os personagens centrais e o arco da história, com mais profundidade.
    Evite spoilers pesados, mas transmita a essência da jornada e do tom da obra.
    Se o livro não for reconhecido, diga que o título parece inválido.
    """
    try:
        modelo = genai.GenerativeModel("gemini-1.5-flash")
        resposta = modelo.generate_content(prompt)
        return resposta.text
    except Exception as e:
        return f"Erro ao gerar resumo: {str(e)}"

# Ação do botão
def ao_clicar():
    titulo = entrada.get()
    if not titulo.strip():
        messagebox.showwarning("Campo vazio", "Por favor, digite o nome de um livro.")
        return

    botao_resumir.config(state=tk.DISABLED)
    texto_resultado.delete('1.0', tk.END)
    status_var.set("Gerando resumo...")
    janela.update_idletasks()

    resumo = obter_resumo(titulo)
    texto_resultado.delete('1.0', tk.END)
    texto_resultado.insert(tk.END, resumo)
    status_var.set("Resumo gerado com sucesso.")
    botao_resumir.config(state=tk.NORMAL)

# Janela principal
janela = tk.Tk()
janela.title("Resumidor de Livros com Gemini IA")
janela.geometry("800x550")
janela.resizable(True, True)

# Estilo moderno
style = ttk.Style()
style.theme_use('clam')
style.configure("TButton", font=("Segoe UI", 11))
style.configure("TLabel", font=("Segoe UI", 11))

# Layout principal
frame = ttk.Frame(janela, padding="15")
frame.grid(row=0, column=0, sticky="nsew")

janela.columnconfigure(0, weight=1)
janela.rowconfigure(0, weight=1)
frame.columnconfigure(2, weight=1)

# Carregar imagem da logo
try:
    imagem_original = Image.open("logo.png")  # Substitua pelo nome correto
    imagem_redimensionada = imagem_original.resize((100, 100))
    imagem_logo = ImageTk.PhotoImage(imagem_redimensionada)

    label_logo = ttk.Label(frame, image=imagem_logo)
    label_logo.image = imagem_logo
    label_logo.grid(row=0, column=0, padx=5, pady=5, sticky="nw", rowspan=2)
except Exception as e:
    print(f"Erro ao carregar a imagem: {e}")

# Campos de entrada e botão
ttk.Label(frame, text="Nome do Livro:").grid(row=0, column=1, padx=5, pady=5, sticky="w")
entrada = ttk.Entry(frame, width=50)
entrada.grid(row=0, column=2, padx=5, pady=5, sticky="ew")

botao_resumir = ttk.Button(frame, text="Gerar Resumo", command=ao_clicar)
botao_resumir.grid(row=1, column=2, padx=5, pady=5, sticky="e")

# Área de texto para resultado
texto_resultado = scrolledtext.ScrolledText(frame, wrap=tk.WORD, width=80, height=20, font=("Segoe UI", 11))
texto_resultado.grid(row=2, column=0, columnspan=3, padx=5, pady=10, sticky="nsew")
frame.rowconfigure(2, weight=1)

# Barra de status
status_var = tk.StringVar()
status_var.set("Pronto.")
barra_status = ttk.Label(janela, textvariable=status_var, relief=tk.SUNKEN, anchor="w", padding=5)
barra_status.grid(row=1, column=0, sticky="ew")

# Atalho com Enter
entrada.bind("<Return>", lambda event: ao_clicar())

# Executar
janela.mainloop()
