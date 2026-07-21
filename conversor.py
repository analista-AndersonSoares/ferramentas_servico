import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image

# Lista global para guardar o caminho das imagens escolhidas
arquivos_selecionados = []

def selecionar_arquivos():
    global arquivos_selecionados
    # Abre uma janela para o usuário selecionar as imagens
    arquivos = filedialog.askopenfilenames(
        title="Selecione as imagens",
        filetypes=[("Imagens", "*.jpg *.jpeg *.png")]
    )
    
    # Se o usuário escolheu algo, atualizamos a lista e o texto na tela
    if arquivos:
        arquivos_selecionados = list(arquivos)
        label_status.config(text=f"{len(arquivos_selecionados)} imagem(ns) selecionada(s)", fg="blue")

def converter_para_pdf():
    # Verifica se o usuário selecionou alguma imagem antes de clicar em converter
    if not arquivos_selecionados:
        messagebox.showwarning("Aviso", "Por favor, selecione as imagens primeiro!")
        return
        
    # Abre uma janela perguntando onde o usuário quer salvar o PDF
    local_salvar = filedialog.asksaveasfilename(
        defaultextension=".pdf",
        filetypes=[("Arquivo PDF", "*.pdf")],
        title="Salvar PDF como"
    )
    
    if not local_salvar:
        return # O usuário cancelou a ação de salvar
        
    try:
        # --- A lógica do Pillow que fizemos anteriormente ---
        primeira_imagem = Image.open(arquivos_selecionados[0]).convert("RGB")
        outras_imagens = []
        
        for arquivo in arquivos_selecionados[1:]:
            img = Image.open(arquivo).convert("RGB")
            outras_imagens.append(img)
            
        primeira_imagem.save(
            local_salvar,
            save_all=True,
            append_images=outras_imagens
        )
        # ---------------------------------------------------
        
        messagebox.showinfo("Sucesso!", "Seu PDF foi criado com sucesso!")
        
        # Limpa o aplicativo para a próxima conversão
        arquivos_selecionados.clear()
        label_status.config(text="Nenhuma imagem selecionada", fg="gray")
        
    except Exception as e:
        # Se algo der errado (ex: arquivo corrompido), mostra o erro na tela
        messagebox.showerror("Erro", f"Ocorreu um erro na conversão:\n{e}")


# --- Configuração da Interface Visual (Janela) ---
janela = tk.Tk()
janela.title("Conversor de Imagem para PDF")
janela.geometry("400x250") # Largura x Altura

# Título dentro do app
titulo = tk.Label(janela, text="Criador de PDF", font=("Arial", 16, "bold"))
titulo.pack(pady=15)

# Botão 1: Selecionar
btn_selecionar = tk.Button(janela, text="1. Selecionar Imagens", command=selecionar_arquivos, width=25)
btn_selecionar.pack(pady=5)

# Texto que mostra quantas imagens foram selecionadas
label_status = tk.Label(janela, text="Nenhuma imagem selecionada", fg="gray")
label_status.pack(pady=5)

# Botão 2: Converter
btn_converter = tk.Button(janela, text="2. Converter e Salvar", command=converter_para_pdf, width=25, bg="#4CAF50", fg="white", font=("Arial", 10, "bold"))
btn_converter.pack(pady=15)

# Mantém a janela aberta rodando
janela.mainloop()