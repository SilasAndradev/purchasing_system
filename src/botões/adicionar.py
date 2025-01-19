import json
from tkinter import messagebox
from tkinter import *
from tkinter import ttk


def adicionar(arquivo, root, frame, side_bar):
    def cancelar():
        adicionar_frame.place_forget()
        frame.grid()
        side_bar.grid()

    def add_produto(arquivo):
        código_igual = False

        try:
            lista = [int(código_entrada.get()), produto_entrada.get(), float(preço_entrada.get())]

        except Exception as e:
            messagebox.showerror("Algo deu errado!", e)

        else:
            try:
                with open(arquivo,'r', encoding="utf-8") as file_add:
                        dado_existente = json.load(file_add)
            except Exception as e:
                messagebox.showerror("Algo deu errado!", e)
            else:    
                for i in dado_existente["produtos"]:
                    if i[0] == lista[0]:
                        código_igual = True

                if not código_igual:
                    if not lista[1].isdigit() and lista[1] != '':
                        dado_existente["produtos"].append(lista)
                        código_entrada.delete(0, END)
                        produto_entrada.delete(0, END)
                        preço_entrada.delete(0, END)
                

                        with open(arquivo, "w", encoding="utf-8") as file_add:
                            json.dump(dado_existente, file_add, indent=4, ensure_ascii=False)

                        messagebox.showinfo("Operação Concluída", "O produto foi adicionado com êxito!")
                    else:
                        messagebox.showerror("Algo deu errado!", "O nome do produto não pode ser um número e não pode estar vazio!")

                else:
                    messagebox.showerror("Algo deu errado!", "Já existe um produto com esse código!")

    with open(arquivo, encoding='utf-8') as file:
            produto = json.load(file)

    frame.grid_remove()
    side_bar.grid_remove()
    adicionar_frame = Frame(root, bg="#363f4e")
    adicionar_frame.place(relx=0.1, rely=0)


    table = ttk.Treeview(adicionar_frame, columns = (1,2,3), show = 'headings')
    table.heading(1, text = 'Código')
    table.heading(2, text = 'Produtos')
    table.heading(3, text = 'Valor')

    for i in produto["produtos"]:
        table.insert(parent = '', index = END, values = (i[0], i[1], f"R$ {i[2]:.2f}"))
        table.grid(row=1, column=0, columnspan=3)

    scrollbar_table = ttk.Scrollbar(adicionar_frame, orient = 'vertical', command = table.yview)
    table.configure(yscrollcommand = scrollbar_table.set)
    scrollbar_table.grid(row=1, column=3)


    código_entrada_label = Label(adicionar_frame, text="Código:")
    código_entrada_label.grid(row=2, column=0, pady=5)

    produto_entrada_label = Label(adicionar_frame, text="Produto:")
    produto_entrada_label.grid(row=3, column=0, pady=5)

    preço_entrada_label = Label(adicionar_frame, text="Preço:")
    preço_entrada_label.grid(row=4, column=0, pady=5)

    código_entrada = Entry(adicionar_frame, width=30)
    código_entrada.grid(row=2, column=1, pady=5)
    
    produto_entrada = Entry(adicionar_frame, width=30)
    produto_entrada.grid(row=3, column=1, pady=5)

    preço_entrada = Entry(adicionar_frame, width=30)
    preço_entrada.grid(row=4, column=1, pady=5)

    enviar_add = Button(adicionar_frame, text='Enviar', command=lambda: add_produto(arquivo))
    enviar_add.grid(row=5, column=1)

    cancelar_add = Button(adicionar_frame, text='Cancelar operação', command=cancelar)
    cancelar_add.grid(row=6, column=1)