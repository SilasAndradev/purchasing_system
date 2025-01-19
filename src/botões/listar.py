import json
from tkinter import *
from tkinter import ttk

def listar(arquivo): 
    """
    Essa função limpa a tela e mostrar quais produtos estão disponíveis, contendo seu nome,
    preço e código.
    """
    with open(arquivo, encoding='utf-8') as file:
            produto = json.load(file)
            
    # setup
    window = Toplevel()
    window.geometry('600x400')
    window.title('Lista dos produtos')

    table = ttk.Treeview(window, columns = (1,2,3), show = 'headings')
    table.heading(1, text = 'Código')
    table.heading(2, text = 'Produtos')
    table.heading(3, text = 'Valor')

    for i in produto["produtos"]:
        table.insert(parent = '', index = END, values = (i[0], i[1], f"R$ {i[2]:.2f}"))
    table.pack(expand = True, fill = 'both')

    scrollbar_table = ttk.Scrollbar(window, orient = 'vertical', command = table.yview)
    table.configure(yscrollcommand = scrollbar_table.set)
    scrollbar_table.place(relx = 1, rely = 0, relheight = 1, anchor = 'ne')