import subprocess
import sqlite3
import os
from tkinter import *
from tkinter import filedialog


lista = []
con = sqlite3.connect('mensagens.db')
cursor = con.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS mensagens (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    arquivo TEXT NOT NULL,
    nome TEXT NOT NULL,
    curso TEXT NOT NULL,
    turma TEXT NOT NULL,
    ano TEXT NOT NULL,
    materia TEXT NOT NULL
);
""")
con.close()

global savedfiles
savedfiles = './Saved Files'
if not os.path.exists(savedfiles):
    os.makedirs(savedfiles)

savedfiles = '\Saved Files'



class Application:
    def __init__(self, master=None):

        self.fonte = ("Verdana", "8")
        self.fonte2 = ("Verdana", "8", "bold")
  
        self.container1 = Frame(master)
        self.container1["pady"] = 5
        self.container1.pack()
        self.container2 = Frame(master)
        self.container2["padx"] = 5
        self.container2["pady"] = 5
        self.container2.pack()
        self.container3 = Frame(master)
        self.container3["padx"] = 5
        self.container3["pady"] = 10
        self.container3.pack()
        self.container4 = Frame(master)
        self.container4["padx"] = 5
        self.container4["pady"] = 10
        self.container4.pack()

        global titulo
        titulo = Label(self.container1, text="Caixa de Entrada")
        titulo["font"] = ("Calibri", "9", "bold")
        titulo.pack()

        self.refresh = Button(self.container2, text="Atualizar", width=10, command= lambda: self.Update())
        self.refresh.grid(row=0, column=1, columnspan=2, pady=10, padx=10)
        
        self.explorer = Button(self.container2, text="Abrir Pasta", command=self.OpenDirectory, width=10)
        self.explorer.grid(row=0, column=3, columnspan=2, pady=10, padx=10)

        self.scrollbar = Scrollbar(master, orient=VERTICAL)

        global listbox
        listbox = Listbox(master, selectmode=SINGLE, yscrollcommand=self.scrollbar.set)
        listbox.pack(side=LEFT, fill=BOTH, expand=1)
        listbox.bind('<<ListboxSelect>>', self.onSelect)
        listbox.bind('<Double-1>', self.DbClick)

        self.scrollbar.config(command=listbox.yview)
        self.scrollbar.pack(side=RIGHT, fill=Y)
 
        global openFile
        openFile = Button(self.container2, text="Abrir", width=10, state=DISABLED, command= lambda: self.Open())
        openFile.grid(row=2, column=1, columnspan=2, pady=10, padx=10)

        global deleteB
        deleteB = Button(self.container2, text="Excluir", width=10, state=DISABLED, command= lambda: self.Delete())
        deleteB.grid(row=2, column=3, columnspan=2, pady=10, padx=10)
        
        
        self.lbl1 = Label(self.container3, text = "Nome: ")
        self.lbl1["font"] = self.fonte2
        self.lbl1.grid(row=0, column=0, sticky=W)
        global nome
        nome = Label(self.container3, text = "")
        nome["font"] = self.fonte
        nome.grid(row=0, column=2, columnspan=3, sticky=W)
        

        self.lbl2 = Label(self.container3, text = "Curso: ")
        self.lbl2["font"] = self.fonte2
        self.lbl2.grid(row=1, column=0, sticky=W)
        global curso
        curso = Label(self.container3, text = "")
        curso["font"] = self.fonte
        curso.grid(row=1, column=2, columnspan=3, sticky=W)
        

        self.lbl3 = Label(self.container3, text = "Turma: ")
        self.lbl3["font"] = self.fonte2
        self.lbl3.grid(row=2, column=0, sticky=W)
        global turma
        turma = Label(self.container3, text = "")
        turma["font"] = self.fonte
        turma.grid(row=2, column=2, sticky=W)
        

        self.lbl4 = Label(self.container3, text = "Ano: ")
        self.lbl4["font"] = self.fonte2
        self.lbl4.grid(row=2, column=3)
        global ano
        ano = Label(self.container3, text = "")
        ano["font"] = self.fonte
        ano.grid(row=2, column=4, sticky=W)
        

        self.lbl5 = Label(self.container3, text = "Materia: ")
        self.lbl5["font"] = self.fonte2
        self.lbl5.grid(row=3, column=0, sticky=W)
        global materia
        materia = Label(self.container3, text = "")
        materia["font"] = self.fonte
        materia.grid(row=3, column=2, columnspan=3, sticky=W)

        self.lbl6 = Label(self.container4, text = "Organizar por: ")
        self.lbl6["font"] = self.fonte2
        self.lbl6.grid(row=4, column=0, sticky=E)

        self.opcoes = ['Mais Recente','Mais Antigo','Nome','Turma','Curso','Ano','Materia']
        global opSelect
        opSelect = StringVar(master)
        opSelect.set(self.opcoes[0])
        global opcao
        opcao = OptionMenu(self.container4, opSelect, *self.opcoes, command=self.OpChange)
        opcao.grid(row=4, column=2, columnspan=3)
        

        #self.test = Button(self.container2, text="Teste", width=10, command= self.Test)
        #self.test.grid(row=4, column=1, columnspan=2, pady=10, padx=10)
        
        self.Update()
        

    def OpChange(self, a):
        self.Update()
        pass
    

    def DbClick(self, evt):
        selection = None
        self.w = evt.widget
        self.index = int(self.w.curselection()[0])
        self.value = self.w.get(self.index)
        selection = str(self.value[0][0])
        self.Open(selection)
        print("Arquivo aberto com duplo clique")
        

    def onSelect(self, evt):
        con = sqlite3.connect('mensagens.db')
        cursor = con.cursor()
        selection = None
        self.w = evt.widget
        self.index = int(self.w.curselection()[0])
        self.value = self.w.get(self.index)
        selection = str(self.value[0][0])
        cursor.execute("SELECT nome FROM mensagens WHERE id LIKE '"+selection+"'")
        self.nome = cursor.fetchone()
        print(selection, self.nome[0])
        con.close()
        deleteB.config(state=NORMAL)
        deleteB.config(command=lambda: self.Delete(selection))
        openFile.config(state=NORMAL)
        openFile.config(command=lambda: self.Open(selection))
        self.UpdateInfo(selection)

        
    def Update(self):
        self.sql_list = [
            "SELECT id FROM mensagens ORDER BY id DESC",
            "SELECT id FROM mensagens",
            "SELECT id FROM mensagens ORDER BY nome COLLATE NOCASE ASC",
            "SELECT id FROM mensagens ORDER BY turma COLLATE NOCASE ASC",
            "SELECT id FROM mensagens ORDER BY curso COLLATE NOCASE ASC",
            "SELECT id FROM mensagens ORDER BY ano COLLATE NOCASE ASC",
            "SELECT id FROM mensagens ORDER BY materia COLLATE NOCASE ASC"
        ]
        
        self.sql_sel = None
        self.op = opSelect.get()
        
        if self.op == "Mais Recente":
            self.sql_sel = self.sql_list[0]

        elif self.op == "Mais Antigo":
            self.sql_sel = self.sql_list[1]

        elif self.op == "Nome":
            self.sql_sel = self.sql_list[2]

        elif self.op == "Turma":
            self.sql_sel = self.sql_list[3]

        elif self.op == "Curso":
            self.sql_sel = self.sql_list[4]

        elif self.op == "Ano":
            self.sql_sel = self.sql_list[5]

        elif self.op == "Materia":
            self.sql_sel = self.sql_list[6]

        else:
            print("Erro")
            
        global lista
        con = sqlite3.connect('mensagens.db')
        cursor = con.cursor()
        self.listanomes = []
        listbox.delete(0, END)
        nome.config(text='')
        curso.config(text='')
        turma.config(text='')
        ano.config(text='')
        materia.config(text='')
        deleteB.config(state=DISABLED)
        openFile.config(state=DISABLED)
        cursor.execute(self.sql_sel)
        lista = cursor.fetchall()
        try:
            for i in range(len(lista)):
                cursor.execute("SELECT nome FROM mensagens WHERE id = " + str(lista[i][0]))
                self.nome = cursor.fetchone()
                cursor.execute("SELECT turma FROM mensagens WHERE id = " + str(lista[i][0]))
                self.turma = cursor.fetchone()
                cursor.execute("SELECT materia FROM mensagens WHERE id = " + str(lista[i][0]))
                self.materia = cursor.fetchone()
                self.tuple = (self.nome[0], self.turma[0], self.materia[0])
                self.string = '  |  '.join(map(str, self.tuple))
                self.newtuple = (lista[i], self.string)
                #print(self.string)
                listbox.insert(END, self.newtuple)
        except:
            titulo.config(text="Erro ao atualizar a lista")
            #print("Erro ao atualizar a lista")
        con.close()
       

            
    def Delete(self, sel):
        try:
            con = sqlite3.connect('mensagens.db')
            cursor = con.cursor()
            cursor.execute("DELETE FROM mensagens WHERE id = "+sel)
            con.commit()
            self.text = str("Arquivo de ID = "+sel+" apagado")
            titulo.config(text=self.text)
            #print("ID: "+sel+" apagado")
            self.Update()
            con.close()
        except:
            titulo.config(text="Erro ao apagar os dados")
            #print("Erro ao deletar os dados")



    def Open(self, sel):
        try:
            con = sqlite3.connect('mensagens.db')
            cursor = con.cursor()
            cursor.execute("SELECT arquivo FROM mensagens WHERE id = "+sel)
            self.filetext = cursor.fetchone()[0]
            con.close()
            #print(self.filetext)
            
            global newwin
            newwin = Toplevel(root)
            newwin.geometry("750x600+10+10")
            
            self.container1 = Frame(newwin)
            self.container1["pady"] = 5
            self.container1.pack()
            self.container2 = Frame(newwin)
            self.container2["pady"] = 5
            self.container2.pack()
            self.container3 = Frame(newwin)
            self.container3["pady"] = 5
            self.container3.pack()
            
            self.title = Label(self.container1, text="Exibindo texto:")
            self.title["font"] = ("Calibri", "9", "bold")
            self.title.pack()

            self.textbox = Text(self.container2, height=32, width=100)
            self.textbox.pack()

            self.save = Button(self.container3, text="Salvar", width=10, command = lambda: self.Save(self.textbox.get("1.0", END)))
            self.save.grid(row=0, column=1, columnspan=2, padx=10)

            #self.exit = Button(self.container3, text="Sair", width=10, command = self.Close)
            #self.exit.grid(row=0, column=3, columnspan=2, padx=10)
            
            self.textbox.insert(END, self.filetext)

            
            
        except:
            titulo.config(text="Erro ao exibir o arquivo")
            print("Erro ao exibir o arquivo")
        

    
    def OpenDirectory(self):
        self.dir_path = os.getcwd() + savedfiles
        subprocess.Popen(['explorer', self.dir_path])
        print(self.dir_path)
        

    def Close(self):
        if newwin:
            newwin.destroy()
            print("Janela fechada")


    def Save(self, text):
        self.dir_path = os.getcwd() + savedfiles
        if newwin:
            self.f = filedialog.asksaveasfile(initialdir = self.dir_path, title = "Selecionar Local", defaultextension = ".txt", filetypes = (("Arquivo de Texto (.txt)", ".txt"),("Documento de Texto (.doc)", ".doc")))
            if self.f is None:
                return
            self.f.write(text)
            self.f.close()
            
    
    def UpdateInfo(self, sel):
        con = sqlite3.connect('mensagens.db')
        cursor = con.cursor()
        cursor.execute("SELECT nome FROM mensagens WHERE id = "+sel)
        self.nome = cursor.fetchone()
        cursor.execute("SELECT curso FROM mensagens WHERE id = "+sel)
        self.curso = cursor.fetchone()
        cursor.execute("SELECT turma FROM mensagens WHERE id = "+sel)
        self.turma = cursor.fetchone()
        cursor.execute("SELECT ano FROM mensagens WHERE id = "+sel)
        self.ano = cursor.fetchone()
        cursor.execute("SELECT materia FROM mensagens WHERE id = "+sel)
        self.materia = cursor.fetchone()
        nome.config(text=self.nome[0])
        curso.config(text=self.curso[0])
        turma.config(text=self.turma[0])
        ano.config(text=self.ano[0])
        materia.config(text=self.materia[0])
        con.close()
        


root = Tk()
menu = Menu(root)
root.config(menu=menu)
root.title("Caixa de Entrada")
root.geometry("420x450+10+10")
Application(root)
root.mainloop()
