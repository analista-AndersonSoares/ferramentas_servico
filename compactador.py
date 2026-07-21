import tkinter as tk
from tkinter import filedialog, messagebox
from pypdf import PdfWriter

arquivos_selecionados = []

def selecionar_arquivos():
    global arquivos_selecionados
    
    arquivos = filedialog.askopenfilenames(
        title="Selecione os relatórios em PDF",
        filetypes=[("Arquivos PDF", "*.pdf")]
    )
    
    if arquivos:
        # Ordena a lista alfabeticamente para garantir a sequência correta das páginas
        arquivos_selecionados = sorted(list(arquivos))
        label_status.config(text=f"{len(arquivos_selecionados)} arquivo(s) selecionado(s)", fg="blue")

def juntar():
    if not arquivos_selecionados:
        messagebox.showwarning("Aviso", "Por favor, selecione os PDFs primeiro!")
        return
        
    # Pergunta onde o usuário quer salvar o arquivo mesclado
    local_salvar = filedialog.asksaveasfilename(
        defaultextension=".pdf",
        filetypes=[("Arquivo PDF", "*.pdf")],
        title="Salvar PDF Mesclado Como"
    )
    
    if not local_salvar:
        return
        
    try:
        merger = PdfWriter()
        
        # O seu loop original, mas agora lendo da lista que o usuário escolheu
        for pdf in arquivos_selecionados:
            merger.append(pdf)
            
        with open(local_salvar, "wb") as saida:
            merger.write(saida)
            
        merger.close()
        
        messagebox.showinfo("Sucesso!", "Os PDFs foram juntados com sucesso!")
        
        # Limpa o app para a próxima tarefa
        arquivos_selecionados.clear()
        label_status.config(text="Nenhum arquivo selecionado", fg="gray")
        
    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro ao processar os arquivos:\n{e}")

# --- Configuração da Interface Visual ---
janela = tk.Tk()
janela.title("Juntar PDF's")
janela.geometry("400x250")

titulo = tk.Label(janela, text="Juntar PDFs", font=("Arial", 16, "bold"))
titulo.pack(pady=15)

btn_selecionar = tk.Button(janela, text="1. Selecionar PDFs", command=selecionar_arquivos, width=25)
btn_selecionar.pack(pady=5)

label_status = tk.Label(janela, text="Nenhum arquivo selecionado", fg="gray")
label_status.pack(pady=5)

btn_juntar = tk.Button(janela, text="2. Juntar e Salvar", command=juntar, width=25, bg="#2196F3", fg="white", font=("Arial", 10, "bold"))
btn_juntar.pack(pady=15)

janela.mainloop()