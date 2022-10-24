from random import randrange
from threading import Timer
from tkinter import *
from tkinter.messagebox import showerror

class SlotMachine:
    def __init__(self):
        self.numeros=["A"]*50+["B"]*40+["C"]*30+["D"]*20+["E"]*10+["F"]*5+["7"]

        self.multiplicadores={
            "A":5,
            "B":10,
            "C":20,
            "D":50,
            "E":200,
            "F":1000,
            "7":100000
        }
    
    #"Spin" na slot machine e obtém os valores resultantes
    def roll(self):
        self.rolled_values=[self.numeros[randrange(156)],self.numeros[randrange(156)],self.numeros[randrange(156)]]
    
    #Retorna os valores rolados
    def get_rolled(self):
        return self.rolled_values

    #Vê se existe prémio e se existir retorna também esse valor
    def qwin_premio(self, aposta):
        self.aposta=aposta
        if self.rolled_values[0]==self.rolled_values[1] and self.rolled_values[1]==self.rolled_values[2]:
            self.premio=self.aposta*self.multiplicadores[self.rolled_values[0]]
            return [True, self.premio]
        else:
            self.premio=0
            return [False, self.premio]

class Jogador:
    def __init__(self,creditos):
        self.creditos=creditos
    
    def get_creditos(self):
        return self.creditos

    def add_creditos(self,cred):
        self.creditos+=cred
    
    def remove_creditos(self,cred):
        self.creditos-=cred

class UI1(Tk):
    def __init__(self):
        super().__init__()
        self.title("Slot Machine")
        self.frame=Frame(self)
        
        self.frame.pack()
        self.geometry("300x110")
        self.eval('tk::PlaceWindow . center')
        self.resizable(False,False)

        #Texto
        self.lbl1=Label(self.frame,text="Quantos créditos quer depositar?", font="none 12")
        self.lbl1.config(anchor=CENTER)
        self.lbl1.pack()

        #Entry Créditos
        self.entry1=Entry(self.frame, font="none 12", justify="center")
        self.entry1.pack(pady=5)

        #Botão Depositar e Enter
        self.btt1=Button(self.frame, text="Depositar", font="none 12 bold", justify="center", command=self.depositar)
        self.btt1.pack(pady=8)

    def depositar(self, evento=0):
        try:
            if int(self.entry1.get())>0:
                self.deposito=int(self.entry1.get())
                self.destroy()
            else:
                showerror(title="Slot Machine", message="Introduza apenas números inteiros positivos!")
        except ValueError:
            showerror(title="Slot Machine", message="Introduza apenas números inteiros positivos!")
    
    def get_deposito(self):
        return self.deposito

class UI2(Tk):
    def __init__(self, deposito):
        super().__init__()
        self.title("Slot Machine")
        self.frame=Frame(self)
        self.frame.pack()
        self.geometry("400x500")
        self.eval('tk::PlaceWindow . center')
        self.resizable(False,False)

        self.jogador=Jogador(deposito)
        self.slots=SlotMachine()

        #Variáveis de texto
        self.slottxt1=StringVar()
        self.slottxt2=StringVar()
        self.slottxt3=StringVar()
        self.win_losetxt=StringVar()
        self.creditostxt=StringVar()
        self.creditostxt.set(f"Créditos: {str(self.jogador.get_creditos())}")
        self.slottxt1.set("7")
        self.slottxt2.set("7")
        self.slottxt3.set("7")
        
        #Título
        self.lbl21=Label(self.frame, text="JACKPOT", justify="center", font="none 40 bold", fg="#FDD835")
        self.lbl21.pack(pady=10)
        
        #Roleta
        self.slot21=Label(self.frame, textvariable=self.slottxt1, font="none 70 bold")
        self.slot21.pack(side=LEFT, expand=YES, fill=BOTH, padx=30)
        self.slot22=Label(self.frame,textvariable=self.slottxt2, font="none 70 bold")
        self.slot22.pack(side=LEFT, expand=YES, fill=BOTH, padx=30)
        self.slot23=Label(self.frame, textvariable=self.slottxt3, font="none 70 bold")
        self.slot23.pack(side=LEFT, expand=YES, fill=BOTH, padx=30)

        #Botão Rolar 
        self.btt21=Button(text=" "*5+"SPIN!"+" "*5, justify="center", font="none 20 bold", command=self.spin)
        self.btt21.pack(pady=10)

        #Texto de Resultados
        self.reslbl=Label(font="none 12 bold",textvariable=self.win_losetxt)
        self.reslbl.pack(pady=5)

        #Valor Aposta
        self.lbl22=Label(font="none 10 bold", text="Valor a apostar:")
        self.lbl22.pack(pady=10)
        self.entry21=Entry(font="none 10", justify="center")
        self.entry21.pack()

        #Botão Sair
        self.btt22=Button(text="SAIR",justify="center", font="none 20", command=self.destroy)
        self.btt22.pack(fill=X, side=BOTTOM)

        #Créditos
        self.credlbl=Label(font="none 10 bold", textvariable=self.creditostxt, justify="center")
        self.credlbl.pack(side=BOTTOM)

    def spin(self):
        #Vê se há créditos suficientes e se houver tira os créditos apostados, só continua se o jogador tiver créditos
        if self.pode_apostar():
            aposta=int(self.entry21.get())
            self.jogador.remove_creditos(aposta)
            
            #Faz os valores do spin e atribui os valores às variáveis de texto
            self.slots.roll()
            valores=self.slots.get_rolled()
            
            self.slottxt1.set(valores[0])
            self.slottxt2.set(valores[1])
            self.slottxt3.set(valores[2])
                

            #Adiciona créditos e vê se o jogador ainda tem créditos, se não tiver termina
            qwin=self.slots.qwin_premio(aposta)
            if qwin[0]:
                self.win_losetxt.set(f"Parabéns! Ganhou {qwin[1]} créditos!")
                self.jogador.add_creditos(qwin[1])
                self.creditostxt.set(f"Créditos: {str(self.jogador.get_creditos())}")
            else:
                self.win_losetxt.set("Perdeu!")
                self.creditostxt.set(f"Créditos: {str(self.jogador.get_creditos())}")
                if self.jogador.get_creditos()==0:
                    showerror(title="Slot Machine", message= "GAME OVER! 0 CRÉDITOS")
                    self.destroy()
    
    #return true ou false dependendo se o jogador pode apostar aquele valor ou não
    def pode_apostar(self):
        try:
            if int(self.entry21.get())>0:
                if int(self.entry21.get())<=self.jogador.get_creditos():
                    return True
                else:
                    showerror(title="Slot Machine", message="Créditos insuficientes")
                    return False
            else:
                showerror(title="Slot Machine", message="Introduza apenas números inteiros positivos!")
                return False
        except ValueError:
            showerror(title="Slot Machine", message="Introduza apenas números inteiros positivos!")
            return False

window_deposito=UI1()
window_deposito.bind("<Return>", window_deposito.depositar)
window_deposito.mainloop()

window_slot=UI2(window_deposito.get_deposito())
window_slot.mainloop()