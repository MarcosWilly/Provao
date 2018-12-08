import subprocess
import sqlite3
import os
from tkinter import *
import shutil
import tkinter.filedialog as fdlg

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


class Application:
    def __init__(self, master=None):
        self.fonte = ("Verdana", "8")
  
        self.container1 = Frame(master)
        self.container1["pady"] = 5
        self.container1.pack()
        self.container2 = Frame(master)
        self.container2["padx"] = 5
        self.container2["pady"] = 5
        self.container2.pack()

        global titulo
        titulo = Label(self.container1, text="Informe os dados:")
        titulo["font"] = ("Calibri", "9", "bold")
        titulo.pack()
  
        self.lbl1 = Label(self.container2, text="Arquivo:", font=self.fonte, width=10)
        self.lbl1.grid(row=0, column=1, sticky=E)
  
        self.filepath = Entry(self.container2, font=self.fonte, width=32)
        self.filepath.grid(row=0, column=2, columnspan=4, sticky=W, pady=25)

        self.explorer = Button(self.container2, text="Buscar", width=10, command= lambda: self.FileSelect(self.filepath))
        self.explorer.grid(row=0, column=6, padx=10)

        self.lbl2 = Label(self.container2, text="Professor:", font=self.fonte, width=10)
        self.lbl2.grid(row=1, column=1, sticky=E)
  
        self.nome = Entry(self.container2, font=self.fonte, width=32)
        self.nome.grid(row=1, column=2, columnspan=4, sticky=W, pady=5)

        self.lbl3 = Label(self.container2, text="Curso:", font=self.fonte, width=10)
        self.lbl3.grid(row=2, column=1, sticky=E)
  
        self.curso = Entry(self.container2, font=self.fonte, width=32)
        self.curso.grid(row=2, column=2, columnspan=4, sticky=W, pady=5)

        self.lbl4 = Label(self.container2, text="Turma:", font=self.fonte, width=10)
        self.lbl4.grid(row=3, column=1, sticky=E)
  
        self.turma = Entry(self.container2, font=self.fonte, width=13)
        self.turma.grid(row=3, column=2, columnspan=2, sticky=W, pady=5)

        self.lbl4 = Label(self.container2, text="Ano:", font=self.fonte, width=10)
        self.lbl4.grid(row=3, column=4, sticky=E)

        self.ano = Entry(self.container2, font=self.fonte, width=7)
        self.ano.grid(row=3, column=5, sticky=E, pady=5)

        self.lbl5 = Label(self.container2, text="Matéria:", font=self.fonte, width=10)
        self.lbl5.grid(row=4, column=1)
  
        self.materia = Entry(self.container2, font=self.fonte, width=32)
        self.materia.grid(row=4, column=2, columnspan=4, sticky=W, pady=5)

        self.enviar = Button(self.container2, text="Enviar", width=10, command= lambda: self.Submit(self.filepath, self.nome, self.curso, self.turma, self.ano, self.materia))
        self.enviar.grid(row=5, column=2, padx=5, sticky=W, pady=15)
        self.limpar = Button(self.container2, text="Limpar", width=10, command= lambda: self.Clear( self.nome, self.curso, self.turma, self.ano, self.materia))
        self.limpar.grid(row=5, column=4, columnspan=2, sticky=E, pady=15)

    
    def FileSelect(self, filepath):
        self.opcoes = {}                 
        self.opcoes['defaultextension'] = '.txt'
        self.opcoes['filetypes'] = [('Documento de Texto','.txt .doc')]
        self.opcoes['initialdir'] = ''    
        self.opcoes['initialfile'] = '' 
        self.opcoes['parent'] = root
        self.opcoes['title'] = ''

        self.arquivo = fdlg.askopenfilename(**self.opcoes)

        if(self.arquivo):
            print(" Arquivo selecionado: "+str(self.arquivo))
            self.info = os.stat(self.arquivo)
            print(str(self.info[6])+" bytes")
            filepath.delete(0, END)
            filepath.insert(0, self.arquivo)

    
    def Submit(self, filepath, nome, curso, turma, ano, materia):
        global savedfiles
        filepath = filepath.get()
        nome = nome.get()
        curso = curso.get()
        turma = turma.get()
        ano = ano.get()
        materia = materia.get()

        if(filepath and nome and curso and turma and ano and materia):
            print("Arquivo: "+filepath+"\n"+nome, curso, turma, ano, materia)
            try:
                con = sqlite3.connect('mensagens.db')
                cursor = con.cursor()
                self.file = open(filepath, 'r')
                self.file = self.file.read()
                cursor.execute("INSERT INTO mensagens (arquivo,nome,curso,turma,ano,materia) VALUES('"+self.file+"','"+nome+"','"+curso+"','"+turma+"','"+ano+"','"+materia+"');")
                con.commit()
                titulo.config(text="Dados enviados com sucesso!")
                con.close()
            except:
                titulo.config(text="Erro ao enviar os dados.")
                #print("\n Erro ao salvar os dados")
        else:
            titulo.config(text="Preencha todos os campos antes de enviar")
            #print(" Preencha todos os campos antes de enviar")


    def Clear(self, nome, curso, turma, ano, materia):
        nome.delete(0, END)
        curso.delete(0, END)
        turma.delete(0, END)
        ano.delete(0, END)
        materia.delete(0, END)
        titulo.config(text="Informe os dados:")





  
  
root = Tk()
menu = Menu(root)
root.title("Enviar Arquivo")
root.config(menu=menu)
Application(root)
root.mainloop()
