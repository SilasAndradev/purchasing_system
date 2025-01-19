# coding=utf-8
import json
from tkinter import messagebox
from tkinter import *
from tkinter import ttk

def home_side_bar(frame, compras_frames):
    compras_frames.place_forget()
    frame.grid()

def finalizar_command(frame, compras_frame, código_inseridos, side_bar, produtos, funcionario):
    home_side_bar(frame, compras_frame)
    heading = ['Produto', 'Valor']
    valor_total_compra = 0
    recibo = ''
    side_bar.grid()
    Pagamento = Toplevel()
    Pagamento.geometry('200x400')
    Pagamento.title('Pagamento')
    
    my_label_head = Label(
    Pagamento, 
    text=f'{heading[0]:<20}{heading[1].center(20)}',
    font=("Helvetrica", 16, "bold"), 
    )

    my_label_head.grid(row=0, column=0, columnspan=2)
    for códigos in enumerate(código_inseridos):
        if códigos[1][1] != None:
            valor_total_compra += códigos[1][2]
            recibo += f'{(códigos[1][1]):<40}{("R$ "+ str(códigos[1][2])).center(40)}\n'
    itens_compra = Label(Pagamento, text=recibo).grid(row=1, column=0, columnspan=2)
    valor_da_compra = Label(Pagamento, text=f"Valor total: R${(valor_total_compra):.2f}",font=("Helvetrica", 12, "bold")).grid(row=2, column=0, columnspan=2)
    vendedor = Label(Pagamento, text=f"O operação de compra foi feita por: {funcionario}", font=("Helvetrica", 12)).grid(row=3, column=0, columnspan=2)
        

def realizarCompra(codigo, arquivo):
    try:
        codigo_input = codigo.get()
        codigo.delete(0, END)

        if not codigo_input.isdigit():
            messagebox.showerror("Erro", "Digite um número inteiro válido.")
            return 0, None, 0

        codigo_produto = int(codigo_input)
        with open(arquivo, encoding='utf-8') as file:
            produtos = json.load(file)["produtos"]

        for item in produtos:
            if int(item[0]) == codigo_produto:
                return int(item[0]), str(item[1]), float(item[2])

        messagebox.showerror("Erro", "Produto não encontrado.")
        return 0, None, 0
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao buscar produto: {str(e)}")
        return 0, None, 0


def comprar(arquivo, root, frame, side_bar, funcionario):
    #------Cores----#
    Lavanda_Avermelhada = "#fff0f5"
    Cinza_Escuro = "#363f4e"
    Azul = "#3f78c1"
    Branco_Neve = "#F0F0EC"
    Sky_Blue = "#87ceeb"
    e9ab89 = "#e9ab89"
    Cinza = "#cccccc"
    Cinza_não_tão_escuro = "#1e1e1e"
    Preto = "#000000"
    Branco = "#FFFFFF"
    cor_principal = Cinza_Escuro
    cor_secundaria = Cinza
    cor_texto = Preto
    cor_texto_fundo = Sky_Blue



    root.config(bg=cor_principal)
    valor_total = 0
    código_inseridos = []
    produto = []
    def atualizarTotal(código_input, nome_produto,valor ):
        nonlocal valor_total
        valor_total += valor
        label_total.config(text=f" {nome_produto} foi adicionado\nValor Total: R$ {valor_total:.2f}")
        if código_input not in código_inseridos:
            produto = [código_input, nome_produto, valor]
            código_inseridos.append(produto)

    # Layout
    frame.grid_remove()
    compras_frame = Frame(root, bg=cor_principal, width=root.winfo_width(), height=root.winfo_height())
    compras_frame.place(relx=0.1, rely=0)

    try:
        with open(arquivo, encoding='utf-8') as file:
            produto = json.load(file)["produtos"]
            produtos = produto
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao carregar produtos: {str(e)}")
        return

    # Tabela
    frame_tabela = LabelFrame(compras_frame, text="Produtos Disponíveis")
    frame_tabela.grid(row=0, column=0, padx=10, pady=10)

    table = ttk.Treeview(frame_tabela, columns=(1, 2, 3), show="headings", height=10)
    table.heading(1, text="Código")
    table.heading(2, text="Produto")
    table.heading(3, text="Preço")
    for item in produtos:
        table.insert("", "end", values=(item[0], item[1], f"R$ {item[2]:.2f}"))

    table.pack(side=LEFT, fill=BOTH, expand=True)
    scrollbar = ttk.Scrollbar(frame_tabela, orient=VERTICAL, command=table.yview)
    table.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side=RIGHT, fill=Y)

    # Entrada e Botões
    codigo = Entry(compras_frame, width=30)
    codigo.grid(row=1, column=0, pady=5)

    buscar = Button(
        compras_frame,
        text="Buscar",
        command=lambda: atualizarTotal(*realizarCompra(codigo, arquivo)),
        bg="#F0F0EC",
        fg="black",
    )
    buscar.grid(row=2, column=0, pady=5)

    finalizar = Button(
        compras_frame,
        text="Finalizar Compra",
        command=lambda: finalizar_command(frame, compras_frame, código_inseridos, side_bar, produtos, funcionario),
        bg="#F0F0EC",
        fg="black",
    )
    finalizar.grid(row=3, column=0, pady=5)


    label_total = Label(compras_frame, text="Valor Total: R$ 0.00", bg="#F0F0EC", fg="black", font=("Arial", 14))
    label_total.grid(row=4, column=0, pady=10)