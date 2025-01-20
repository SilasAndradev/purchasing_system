# coding=utf-8
from tkinter import *
import json
from PIL import ImageTk, Image, ImageDraw
from botões.listar import listar
from botões.comprar import comprar
from botões.adicionar import adicionar
from tkinter import messagebox


#-----Funções-----#
def botoes_arredondados_image(width, height, radius, color):
    """
    Cria uma imagem com bordas arredondadas
    """
    image = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    draw.rounded_rectangle((0, 0, width, height), radius=radius, fill=color)
    return image


def logar():
    global permissão
    usuario = login_usuario.get()
    senha = login_senha.get()
    global funcionario

    try:
        with open(produtos, encoding='utf-8') as file:
            vendedores = json.load(file)["vendedores"]

    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao carregar os vendedores: {str(e)}")
    else:
        for vendedor in vendedores:
            if usuario == vendedor[1] and senha == vendedor[2]:
                if vendedor[0] >= 2000:
                    permissão = True 
                    funcionario = vendedor[1] + ', o Moderador'
                else:
                    permissão = True 
                    funcionario = vendedor[1]

                login_senha.delete(0, END)
                login_usuario.delete(0, END)

                login.grid_remove()

                home.grid(row=0, column=1)
                side_bar.grid(row=0, column=0,)

                listar_produtos.place(relx=0.3, rely=0.5, anchor=CENTER)
                comprar_produtos.place(relx=0.5, rely=0.5, anchor=CENTER)
                adicionar_produtos.place(relx=0.7, rely=0.5, anchor=CENTER)


                home_b.grid(row=0,column=0,pady=10)
                set_b.grid(row=1,column=0,pady=10)
                leave_b.grid(row=2, column=0, pady=10)

                messagebox.showinfo("Bem-vindo", f"É bom ver você de volta, {vendedor[1]}!")
                break
            elif usuario == vendedor[1] and senha != vendedor[2]:
                messagebox.showerror("Algo de errado!","A senha está incorreta!")
                break

def leave_side_bar():
    home.grid_remove()
    side_bar.grid_remove()
    login.grid()


def expand():
    global cur_width, expanded
    cur_width += 10
    rep = master.after(5,expand) 
    side_bar.config(width=cur_width)
    if cur_width >= max_w:
        expanded = True
        master.after_cancel(rep)
        fill()

def contract():
    global cur_width, expanded
    cur_width -= 10
    rep = master.after(5,contract)
    side_bar.config(width=cur_width)
    if cur_width <= min_w:
        expanded = False
        master.after_cancel(rep)
        fill()

def fill():
    if expanded:
        home_b.config(text='Home', image='', font=("Helvetica",21), fg=cor_texto, bg = Branco_Neve)
        set_b.config(text='Configurações', image='', font=("Helvetica",21), fg=cor_texto, bg = Branco_Neve)
        leave_b.config(text='Sair', image='', font=("Helvetica",21), fg=cor_texto, bg = Branco_Neve)

    else:
        home_b.config(image=home_icon,font=(0,21), bg = Sky_Blue)
        set_b.config(image=settings_icon,font=(0,21), bg = Sky_Blue)
        leave_b.config(image=sair_icon,font=(0,21), bg = Sky_Blue)

def home_side_bar(master, home, side_bar):
    for widgets in master.winfo_children():
        widgets.grid_remove()
    home.grid()
    master.update()
    side_bar.grid()

def settings_side_bar(settings, home):
    side_bar.grid_remove()
    home.grid_remove()
    settings.grid(row=0, column=1)
    side_bar.grid()
    
def close_side_bar(side_bar):
    side_bar.grid_remove()
    

#----------Tkinter----------#
master = Tk()
master.title("Sistema de Compras")
master.geometry('800x600')
master.minsize(600, 100)
master.iconbitmap("TKINTER/Sistema_Compras/assets/icon.ico")


#----------Cores----------#
Cinza_Escuro = "#363f4e"

Branco_Neve = "#F0F0EC"
Sky_Blue = "#87ceeb"
Cinza = "#cccccc"
Preto = "#000000"

cor_principal = Cinza_Escuro
cor_secundaria = Cinza
cor_texto = Preto
cor_texto_fundo = Sky_Blue



master.config(bg=cor_principal)

#-------Variáveis-------#
expanded = False
permissão = False


#-----Botões arredondados----#
button_image_login = botoes_arredondados_image(100, 25, 20, cor_texto_fundo)
button_photo_login = ImageTk.PhotoImage(button_image_login)
button_image_passar = botoes_arredondados_image(120, 25, 20, cor_texto_fundo)
button_photo_passar = ImageTk.PhotoImage(button_image_passar)

#-------Constantes-------#
produtos = 'TKINTER/Sistema_Compras/assets/produtos.json'
min_w = 50
max_w = 200
cur_width = min_w

#----------Frames----------#
settings = Frame(master, bg=cor_principal, width=master.winfo_width(), height=master.winfo_height())
side_bar = Frame(master,bg=cor_secundaria, width=50, height=master.winfo_height())
home = Frame(master, bg=cor_principal, width=master.winfo_width(), height=master.winfo_height())
login = Frame(master, bg=cor_principal, width=master.winfo_width(), height=master.winfo_height())

#----------Imagens---------#
adicionar_icon = ImageTk.PhotoImage(Image.open("TKINTER/Sistema_Compras/assets/adicionar.png"))
lista_icon = ImageTk.PhotoImage(Image.open("TKINTER/Sistema_Compras/assets/listar.png"))
comprar_icon = ImageTk.PhotoImage(Image.open("TKINTER/Sistema_Compras/assets/comprar.png").resize((128,128)))
home_icon = ImageTk.PhotoImage(Image.open('TKINTER/Sistema_Compras/assets/home.png').resize((40,40)))
settings_icon = ImageTk.PhotoImage(Image.open('TKINTER/Sistema_Compras/assets/settings.png').resize((40,40)))
sair_icon = ImageTk.PhotoImage(Image.open('TKINTER/Sistema_Compras/assets/sair.png').resize((40,40)))


#----------Botões----------#
listar_produtos = Button(home, image = lista_icon, compound=LEFT, command=lambda: listar(produtos))
comprar_produtos = Button(home, image = comprar_icon, compound=LEFT, command=lambda: [close_side_bar(side_bar) ,comprar(produtos, master, home, side_bar, funcionario)])
adicionar_produtos = Button(home, image = adicionar_icon, compound=LEFT, command=lambda: adicionar(produtos, master, home, side_bar))

#---------Side Bar---------#
master.update()

home_b = Button(side_bar, 
    image=home_icon,
    bg= cor_texto_fundo,
    relief='flat', 
    command= lambda: home_side_bar(master, home, side_bar))

set_b = Button(side_bar, 
    image=settings_icon, 
    bg= cor_texto_fundo,
    relief='flat', command= lambda: settings_side_bar(settings, home))

leave_b = Button(side_bar, 
    image=sair_icon, 
    bg= cor_texto_fundo,
    relief='flat', command= lambda: leave_side_bar())


side_bar.bind('<Enter>', lambda e: expand())
side_bar.bind('<Leave>', lambda e: contract())

side_bar.grid_propagate(False)

#-----------login---------#
#login.grid(row=0, column=0, rowspan=5, columnspan=5)

login.grid(row=0, rowspan=5, column=0, columnspan=5)
login_usuario = Entry(login,width=30)
login_senha = Entry(login, width=30, show="*")
login_botão = Button(login, image=button_photo_login, pady=5, command= logar, text="Logar", font=("Arial", 12, "bold"), fg=cor_texto, bd=0, compound="center", bg=Cinza_Escuro, activebackground=Cinza_Escuro)


login_usuario.place(relx=0.5, rely=0.25, anchor=CENTER,relheight=0.05)
login_senha.place(relx=0.5, rely=0.32, anchor=CENTER, relheight=0.05)
login_botão.place(relx=0.5, rely=0.39, anchor=CENTER, relheight=0.05)


master.mainloop()