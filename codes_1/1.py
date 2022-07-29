"""**********************************************************************************************************************"""
"""***********************************************Lexer Başlangıcı***********************************************"""

import lex

### Tokenlerin Listelenmesi ###

tokens = ['NUMBER',
        'LBRACKET',
        'RBRACKET',
        'FORWARD',
        'RIGHT',
        'LOOP',
        'COLOR',
        'PEN',
        'PEN_COLOR'] 


class datas:
    command_list = []
    current_index = 0
    is_error = False

komutlar = datas()

### Tokenlerin Tanımlanması ###

pos=[]
def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    pos.append(t.lexpos)
    komutlar.command_list.append(t.value)
    return t


def t_LBRACKET(t):
    r'\['
    return t

def t_RBRACKET(t):
    r'\]'
    komutlar.current_index -= 1
    komutlar.command_list.append("For%d out" % (komutlar.current_index))
    return t

def t_COLOR(t):
    r'COLOR'
    komutlar.command_list.append("COLOR")
    return t

def t_PEN_COLOR(t):
    r'[KMSY]'
    komutlar.command_list.append(t.value)
    return t

def t_FORWARD(t):
    r'F'
    komutlar.command_list.append("F")
    return t

def t_PEN(t):
    r'PEN'
    komutlar.command_list.append('PEN')
    return t

def t_RIGHT(t):
    r'R'
    komutlar.command_list.append("R")
    return t

def t_LOOP(t):
    r'L'
    komutlar.command_list.append("For%d in" % (komutlar.current_index))
    komutlar.current_index += 1
    return t

t_ignore  = ' \n'

### Tanımlanamayan Karakter Hatasının Tanımlanması ###

illegalc = 0
error_counter = 1.0
def t_error(t):
    global error_counter
    global illegalc
    if dil.get() == 1:
        if illegalc == 0:
            hata.configure(state='normal')
            hata.insert(str(error_counter), "Illegal Character Error:\n")
            hata.configure(state='disabled')
            error_counter += 1
            illegalc += 1
        if is_fixing_var.get() == False:
            hata.configure(state='normal')
            hata.insert(str(error_counter), f"{t.value[:1]} is a illagel character in index number {t.lexpos} \n")
            hata.configure(state='disabled')
            error_counter += 1
            komutlar.is_error = True
        elif is_fixing_var.get() == True:
            pass
        t.lexer.skip(1)
    else:
        if illegalc == 0:
            hata.configure(state='normal')
            hata.insert(str(error_counter), "Tanımlanamayan Karakter Hatası:\n")
            hata.configure(state='disabled')
            error_counter += 1
            illegalc += 1
        if is_fixing_var.get() == False:
            hata.configure(state='normal')
            hata.insert(str(error_counter), f"{t.lexpos} indeksindeki {t.value[:1]} karakteri yanlış!\n")
            hata.configure(state='disabled')
            error_counter += 1
            komutlar.is_error = True
        elif is_fixing_var.get() == True:
            pass
        t.lexer.skip(1)

lexer = lex.lex()

"""**********************************************************************************************************************"""
"""***********************************************Parserx Başlangıcı***********************************************"""

import yacc

### Söz Dizimi Hatası için Parse Ağacı Oluşturulması ###

def p_expressions(p):
    '''expression : expression fw  
    | expression color  
    | expression turn 
    | expression for_loop
    | expression pen_pick
    | empty'''


def p_empty(p):
    'empty :'
    pass

### Kalınlık Hatasının Tanımlanması ###
pencounter = True
def p_pen_pick(p):
    '''pen_pick : PEN NUMBER'''
    global error_counter
    global pencounter 
    if p[2] > 3:
        if dil.get() == 1:
            if pencounter == True:
                hata.configure(state='normal')
                hata.insert(str(error_counter), "Thickness Error: \n")
                hata.configure(state='disabled')
                error_counter += 1
                pencounter = False
            hata.configure(state='normal')
            hata.insert(str(error_counter), f"{p[2]} is a unwanted thickess value in index {pos[-1]} \n")
            hata.configure(state='disabled')
            komutlar.is_error = True
            error_counter += 1            
        else:
            if pencounter == True:
                hata.configure(state='normal')
                hata.insert(str(error_counter), "Kalınlık Hatası: \n")
                hata.configure(state='disabled')
                error_counter += 1
                pencounter = False
            hata.configure(state='normal')
            hata.insert(str(error_counter), f"{pos[-1]} indeksindeki {p[2]} kalınlığı istenilen değerlerin dışında!\n")
            hata.configure(state='disabled')
            komutlar.is_error = True
            error_counter += 1



def p_forward(p):
    '''fw : FORWARD NUMBER'''


def p_for_loop(p):
    '''for_loop : LOOP NUMBER LBRACKET expression RBRACKET'''


def p_turn(p):
    'turn : RIGHT NUMBER'


def p_color_pick(p):
    '''color : COLOR PEN_COLOR '''

### Söz Dizimi Hatasının Tanımlanması ###

pcounter = 0
def p_error(p):
    global pcounter
    global error_counter
    if dil.get() == 1:
        if pcounter == 0:
            hata.configure(state='normal')
            hata.insert(str(error_counter), "Grammar Error:\n")
            hata.configure(state='disabled')
            error_counter += 1
            if bracket_control.count("[") != bracket_control.count("]"):
                hata.configure(state='normal')
                hata.insert(str(error_counter), f"Number of Right and Left parenthesis are not equal!\n")
                hata.configure(state='disabled')
                error_counter += 1
            hata.configure(state='normal')
            hata.insert(str(error_counter), f"{p.value} value is againts our grammar rules in index {p.lexpos}!\n")
            hata.configure(state='disabled')
            pcounter += 1
            error_counter += 1    
    else:
        if pcounter == 0:
            hata.configure(state='normal')
            hata.insert(str(error_counter), "Söz Dizimi Hatası:\n")
            hata.configure(state='disabled')
            error_counter += 1
            if bracket_control.count("[") != bracket_control.count("]"):
                hata.configure(state='normal')
                hata.insert(str(error_counter), f"Sol ve Sağ parantez sayısı eşit değil!\n")
                hata.configure(state='disabled')
                error_counter += 1
            hata.configure(state='normal')  
            hata.insert(str(error_counter), f"{p.lexpos} indeksindeki {p.value} karakteri gramer kurallarimiza aykiri!\n")
            hata.configure(state='disabled')
            pcounter += 1
            error_counter += 1

    komutlar.is_error = True
    print("Syntax error in input!")


parser = yacc.yacc()


"""**********************************************************************************************************************"""
"""***********************************************Turtle Başlangıcı***********************************************"""

import turtle
import math

def pen_picking(ressam,thickness):
    ressam.width(thickness)
    return

def color_picking(ressam,color):
    if color == "K":
        ressam.color("red")
        return
    elif color == "Y":
        ressam.color("green")
        return
    elif color == "M":
        ressam.color("blue")
        return
    elif color == "S":
        ressam.color("black")
        return

def turn_right(ressam,degree):
    ressam.right(degree)


def ressam_forward(ressam,step):
    global oran
    ressam.speed(ressam_hiz())
    ressam.forward(step*(oran/10))


def for_out_finder(command_list: list,for_level: str):
    for_looking = for_level.split()[0]+" out"
    for i,deger in enumerate(command_list):
        if deger == for_looking:
            return i


def parsing_func(command_listx: list,ressam):
    global is_continue
    if not is_continue:
        return
    command_list = command_listx
    ressam.showturtle()
    i = 0
    while len(command_list) != 0:
        command = command_list[i]
        if command == "F":
            step = command_list[i+1]
            ressam_forward(ressam,step)
            del command_list [i:i+2]
        elif command == "PEN":
            thickness = command_list[i+1]
            pen_picking(ressam,thickness)
            del command_list [i:i+2]
        elif command == "COLOR":
            color = command_list[i+1]
            color_picking(ressam,color)
            del command_list[i:i+2]
        elif command == "R":
            degree = command_list[i+1]
            turn_right(ressam,degree)
            del command_list[i:i+2]
        elif "in" in str(command):
            for_out_index = for_out_finder(command_list,command)
            for z in range(command_list[i+1]):
                parsing_func(command_list[i+2:for_out_index],ressam)
            del command_list[i:for_out_index+1]
    ressam.hideturtle()


def ressam_hiz():
    cizim_hizi = hiz_duzenle.get()
    if cizim_hizi == 11:
        cizim_hizi = 0
    ressam.speed(hiz_duzenle.get())


canvas_datas = {'currentDegree':0,'x_step':0,'y_step':0,'error_flag':False}

def calculate_canvas(command_listx: list):
    global canvas_datas
    global oran
    command_list = command_listx.copy()
    i = 0
    while len(command_list) != 0:
        command = command_list[i]
        if command == "F":
            step = command_list[i+1] * (oran/10)
            div_pi = canvas_datas['currentDegree']/180
            canvas_datas['x_step'] += step * (math.cos(math.pi*div_pi))
            canvas_datas['y_step'] += step * (math.sin(math.pi*div_pi))
            del command_list [i:i+2]
        elif command == "PEN":
            del command_list [i:i+2]
        elif command == "COLOR":
            del command_list[i:i+2]
        elif command == "R":
            canvas_datas['currentDegree'] += command_list[i+1]
            del command_list[i:i+2]
        elif "in" in str(command):
            for_out_index = for_out_finder(command_list,command)
            for z in range(command_list[i+1]):
                calculate_canvas(command_list[i+2:for_out_index])
            del command_list[i:for_out_index+1]
    if not (-746.25/2  < canvas_datas['x_step'] < 746.25/2) or not (-742.5/2 < canvas_datas['y_step'] < 742.5/2):
        canvas_datas['error_flag'] = True


def log_ekrani(satir,metin):
        hata.configure(state='normal')
        hata.insert(str(satir), metin+"\n")
        hata.configure(state='disabled')


satir = 1.0
def log_yazdir(yapilacaklar: list):
    global satir
    index = 0
    command_list = yapilacaklar.copy()
    i = 0
    while len(command_list) != 0:
        command = command_list[i]
        if command == "F":
            step = command_list[i+1]
            if dil.get() == 1:
                log_ekrani(satir," "*index + f"{str(step)} step forward.")
            else:
              log_ekrani(satir," "*index + f"{str(step)} Adım ilerlendi.")
            satir += 1.0
            del command_list [i:i+2]
        elif command == "PEN":
            thickness = command_list[i+1]
            if dil.get() == 1:
                log_ekrani(satir," "*index + f"Pen thickness turns{str(thickness)} .")
            else:
                log_ekrani(satir," "*index + f"Kalem kalınlığı {str(thickness)} yapıldı.")
            satir += 1.0
            del command_list [i:i+2]
        elif command == "COLOR":
            color = command_list[i+1]
            if dil.get() == 1:
                log_ekrani(satir," "*index + f"Pen color turns {str(color)}.")
            else:
                log_ekrani(satir," "*index + f"Kalem rengi {str(color)} yapıldı.")
            satir += 1.0
            del command_list[i:i+2]
        elif command == "R":
            degree = command_list[i+1]
            if dil.get() == 1:
                log_ekrani(satir," "*index + f"Turns {str(degree)} degree right.")
            else:
              log_ekrani(satir," "*index + f"{str(degree)} Derece sağa dönüldü.")
            satir += 1.0
            del command_list[i:i+2]
        elif "in" in str(command):
            loop_number = command_list[i+1]
            if dil.get() == 1:
                log_ekrani(satir," "*index + f"Looped {str(loop_number)} times.")
            else:
                log_ekrani(satir," "*index + f"{str(loop_number)} Defa for döngüsü çalıştı.")
            satir += 1.0
            index += 2
            del command_list[i:i+2]
        elif "out" in str(command):
            index -= 2
            if dil.get() == 1:
                log_ekrani(satir," "*index + f"Exit from for loop.")
            else:
                log_ekrani(satir," "*index + f"For döngüsünden çıkıldı.")
            satir += 1.0
            del command_list[i:i+1]
            

"""**********************************************************************************************************************"""
"""***********************************************Gui Başlangıcı***********************************************"""

from tkinter import *
from tkinter import filedialog
import customtkinter
from customtkinter import *
import os


customtkinter.set_default_color_theme("green") 

ekran = CTk()
ekran.configure(background='#616161')
ekran.title('UwU *RobArt* UwU')
ekran.maxsize(1200,750)
ekran.minsize(1200,750)

is_continue = True

### Hatalar Ekranına Metin Yazdıran Fonksiyonu ###

def hatalar_yazdir(metin):
    global error_counter
    hata.configure(state='normal')
    hata.insert(str(error_counter), metin+"\n")
    hata.configure(state='disabled')
    error_counter += 1

### Başlatmadan Önce Sıfırlama Fonksiyonu ### 

def sifirla():
    global canvas_datas
    canvas_datas['currentDegree'] = 0
    canvas_datas['x_step'] = 0
    canvas_datas['y_step'] = 0
    canvas_datas['error_flag'] = False
    global is_continue
    komutlar.is_error = False
    is_continue = True
    komutlar.command_list = []
    ressam.reset()
    global illegalc
    illegalc = 0
    global pencounter
    pencounter = True
    global pcounter
    pcounter = 0


### Başlatma Butonu Fonksiyonu ###
oran = 0
bracket_control = None 
def start(ressam,dosya_yolu):
    sifirla()
    if dosya_yolu == "":
        return
    global oran
    global bracket_control
    oran = b.get()
    baslat.configure(state = DISABLED)
    b_emek.configure(state=DISABLED)
    command_txt = open(dosya_yolu,"r").read().strip()
    bracket_control = command_txt
    txt_komut.configure(state='normal')
    txt_komut.delete("1.0",END)
    txt_komut.insert("1.0",command_txt)
    txt_komut.configure(state="disabled")
    hata.configure(state='normal')
    hata.delete("1.0",END)
    hata.configure(state='disabled')
    if command_txt.isupper() == False:
        global error_counter
        hata.configure(state='normal')
        hata.delete("1.0",END)
        if dil.get() == 1:
            hata.insert(str(error_counter), "\nThere are lowercased charaters in text but we fixed them for you ;)\n")
        else:
            hata.insert(str(error_counter), "\nKomutlarda küçük karakterler var fakat biz bunları sizin için büyüttük ;)\n")
        hata.configure(state='disabled')
        command_txt = command_txt.upper()
    parser.parse(command_txt)
    if komutlar.is_error:
        return

    ressam.home()
    ressam.clear()
    calculate_canvas(komutlar.command_list)
    if canvas_datas['error_flag']:
        hata.configure(state='normal')
        if dil.get() == 1:
            hata.insert(str(error_counter), "Out of Border Error:\n")
            error_counter += 1
            hata.insert(str(error_counter), "Drawing does not fit into the canvas. Plase change size of the drawing or decrase the numbers.\n")
            hata.configure(state='disabled')
            error_counter += 1
            baslat.configure(state = NORMAL)
            return
        else:
            hata.insert(str(error_counter), "Sınır Hatası:\n")
            error_counter += 1
            hata.insert(str(error_counter), "Çizilecek şekil ekrana sığmıyor. Lütfen oranı değiştirin veya sayılarınızı küçültün.\n")
            hata.configure(state='disabled')
            error_counter += 1
            baslat.configure(state = NORMAL)
            return
    log_yazdir(komutlar.command_list)
    parsing_func(komutlar.command_list,ressam)
    baslat.configure(state = NORMAL)
    b_emek.configure(state= NORMAL)


### Ana Pencere ###

pencere =CTkCanvas(ekran,height=750,width=1200,bg="#616161")
pencere.pack()

### Sol Üst Kısım ###

solu_kisim =CTkFrame(ekran, bg='DimGray')
solu_kisim.place(relx=0.003125,rely=0.005,relwidth=0.36875,relheight=0.58)


### Sağ Kısım  Frame ###

sag_kisim =CTkFrame (ekran, bg='DimGray')
sag_kisim.place(relx=0.375,rely=0.005,relwidth=0.621875,relheight=0.990)

### Komut Dosyası Seçiniz ###

komut=CTkLabel(solu_kisim,text="Komut dosyasını seçiniz",width=18,text_font=("Helvetica",-16))
komut.place(x=2,y=11)

### Dosya Seçme Fonksiyonu ###

def dosya_sec():
    dosyam = filedialog.askopenfilename(filetypes=[("Text Files","*.txt")])
    adres.config(state=NORMAL)
    adres.delete(0,END)
    adres.insert(0,dosyam)
    adres.config(state=DISABLED)
    baslat.configure(state = NORMAL)
    komutlar.is_error = False

### Dosya Yolu Kısmı ### 

adres = CTkEntry(solu_kisim,text="",width=175)
adres.config(state=DISABLED)
adres.place(x=185,y=10)


### Dosya Seçme Butonu ###

secim = CTkButton (solu_kisim,text='Seç',command=dosya_sec,width=57,text_font=("Helvetica",-14))
secim.place(x=367,y=10)


### Çizim Hızı Başlangıç ###

cizim_hiz=CTkLabel(solu_kisim,text="Çizim Hızı",width=10,text_font=("Helvetica",-16))
cizim_hiz.place(x=2,y=50)


h=IntVar()
h.set(6)
def hiz(deger):
    CTkLabel(solu_kisim,text=h.get(),width=20,bg="DimGray",text_font=("Helvetica",-15)).place(x=390,y=75)

### Çizim Hızı Label ###

hiz_duzenle = CTkSlider(solu_kisim,from_=1, to=11, number_of_steps= 10,variable=h,command=hiz,width=370,progress_color="#11B384")
hiz_duzenle.place(x=20,y=80)


### Çizim Oranı Başlangıç ###

b=IntVar()
b.set(10)
def buyukluk(deger):
    label_deger = b.get() /10
    CTkLabel(solu_kisim,text=label_deger,width=20,bg="DimGray",text_font=("Helvetica",-15)).place(x=390,y=135)


cizim_oran=CTkLabel(solu_kisim,text="Çizim Büyüklüğü",width= 100,text_font=("Helvetica", -16))
cizim_oran.place(x=1,y=110)

buyukluk_duzenle = CTkSlider(solu_kisim,from_=1, to=20, number_of_steps= 19,variable=b,command=buyukluk,width=370,progress_color="#11B384")

buyukluk_duzenle.place(x=20,y=140)


### Olası Hatalar Kısmı ### 

olasi_hata =CTkLabel(solu_kisim,text='Olası hatalar gidelirmeye çalışılsın',bg='DimGray',text_font=("Helvetica",-16))
olasi_hata.place(x=65,y=170)

is_fixing_var = BooleanVar()
is_fixing= CTkCheckBox(solu_kisim,variable=is_fixing_var,bg="DimGray",onvalue=True,offvalue=False,text="")
is_fixing.place(x=320,y=170)


### Çizimi Başlat Butonu ###

baslat =CTkButton (solu_kisim,width=180,text= "Çizimi Başlat" ,command=lambda: start(ressam,adres.get()),text_font=("Helvetica",-15)) 
baslat.place(x=25, y=207)


### Çizimi Durdur ###

def durdur():
    global is_continue
    is_continue = False

durdur_surdur = CTkButton(solu_kisim,width=180,text= "Çizimi Durdur",text_font=("Helvetica",-15),command = durdur)
durdur_surdur.place(x=233, y=207)

### Txt İçeriği ###

txt_icerik= CTkLabel(solu_kisim,text="Komut Dosyası İçeriği",width=50,text_font=("Helvetica",-16))
txt_icerik.place(x=2,y=248)
txt_komut= Text(solu_kisim,bg='#616161',height=8,width=50,fg='white',borderwidth=0)
txt_komut.place(x=20,y=285)
txt_komut.configure(state="disabled")

### Sol Alt Kısım Ekranı ###

sola_kisim =CTkFrame (ekran, bg='DimGray')
sola_kisim.place(relx=0.003125,rely=0.590,relwidth=0.36875,relheight=0.405)

### Log İçeriği ###

log=CTkLabel(sola_kisim,text="Loglar",width=10,bg='DimGray',text_font=("Helvetica",-16))
log.place(x=3,y=10)
hata = Text(sola_kisim,bg='#616161',height=12,width=50,fg='white',borderwidth=0)
hata.configure(state="disabled")
hata.pack(padx=2,pady=45)

### Dark-Light ###

def mode():
    if mode.get() == 1:
        customtkinter.set_appearance_mode("light")
    
    else :
        customtkinter.set_appearance_mode("dark")
        


mode=CTkSwitch(sola_kisim,text="Light/Dark",command=mode,button_color='#11B384', text_font=('Helvetica',-12))
mode.place(x=8,y=247)


### Kullanım Kılavuzu ###

def sayfa_ac():
    pencere.grab_set()
    global yeni
    yeni = CTkToplevel(pencere)
    def destroy_it():
        pencere.grab_release()
        yeni.destroy()
    yeni.protocol("WM_DELETE_WINDOW", destroy_it)
    yeni.title("Kullanım Kılavuzu")
    yeni.maxsize(1200,750)
    yeni.minsize(1200,750)
    yeni.geometry("+150+50")
    
    frame1 = CTkFrame(yeni,height=730,width=1180)
    frame1.place(x=10,y=10)
    baslik = CTkLabel(frame1,text= """ Kullanım Kılavuzu """,text_font=('Helvetica',-20))
    baslik.place(x=220,y=10)
    baslik2 = CTkLabel(frame1,text= """ User Guide """,text_font=('Helvetica',-20))
    baslik2.place(x=820,y=10)
    
    t1 = Text(frame1,width=70,height=39,bg='#656565',fg='white',border=0,font=('Helvetica',11))
    t1.place(x=22,y=42)
    syf_1 = """
     Kullanım Kılavuzu

 1.1  Programımız ne yapar?
 1.2  Komutlar
 1.3  Hatalar
 1.4  Program Ayarları
 1.5  Programın Çalıştırılması 

 1.1 Programımız ne yapar?
   
   Kullanıcıdan alınan komutlar doğrultusunda istenilen şekli çizer.

 1.2 Komutlar
   
   F : F harfi kaç adım ileri çizeceğini belirtir. F’nin yanına ileri yönde çizilecek adım sayısı yazılmalıdır.

        Örnek : F 42  -> 42 Adım ileri yönde çizecektir.
   
   R : R harfi RobArt’ımızın kaç derece sağa dönüleceğini belirtir. R’nin yanına kaç derece döndürüleceği yazılmalıdır.
   
        Örnek : R 61  -> RobArt, 61 derece sağa dönecektir.
   
   L : L harfi döngüyü simgelemektedir. Köşeli parantezler içerisine aldığı komutların kaç defa tekrar edileceğini belirtir.
 
        Örnek : L 27 [F 5 R9] -> RobArt, 27 defa 5 adım ilerleyip 9 derece sağa dönecektir.
   
   COLOR : COLOR kelimesi RobArt’ın kaleminin hangi rengi alacağını belirtir. 
  
      RobArt’ın 4 renk kalemi bulunmaktadır. Bunlar aşağıdaki gibidir:
	      K -> Kırmızı
	      Y -> Yeşil
	      M -> Mavi
	      S -> Siyah

        Örnek : COLOR M -> RobArt mavi kalemi seçecektir.
   
    PEN : Pen kelimesi RobArt’ın kaleminin kalınlığını belirler. RobArt’ın 3 farklı kalınlıkta kalemi vardır. Bunlar aşağıdaki gibidir:
	      1 -> İnce
	      2 -> Normal
	      3 -> Kalın

        Örnek: PEN 3 -> RobArt kalın kalemi seçecekti
    
 1.3 Hatalar

  - RobArt küçük karakterle girilebilecek her ifadeyi büyültür. 

  - Tanımlanamayan Karakter: Verilen komut dosyasında RobArt’ın tanımadığı bir karakter yer alır.

  - Söz Dizimi Hatası: Verilen komut dosyasında yukarıdaki komut kullanımları dışında bir kullanım olduğunda söz dizimi hatası alınır.

  - Kalınlık Hatası: Verilen komut dosyasında yukarıdaki kalınlıkların dışında kalınlık seçimi olduğunda kalınlık hatası alınır.
  
  - Sınır İhlali Hatası:Komut dosyasındaki komutlar yardımıyla çizilmesi istenilen çizimin tuvale sığmaması durumudur.


 1.4 Program Ayarları

   - Çizim Hızı: RobArt ile çizilmesi istenen çizimin hızı ayarlanır.
 
   - Çizim Büyüklüğü: RobArt ile çizilmesi istenen çizimin büyüklüğü ayarlanır.

   - Olası Hatalar Giderilmeye Çalışılsın: Bu seçenek seçildiği takdirde RobArt tanımlanamayan karakterleri yok edecektir.


 1.5 Programın Çalıştırılması 

   Program açıldıktan sonra “Seç” butonu ile çizilmesi istenilen komut dosyası seçilir. Ardından isteğe olası hataların giderilmesi isteğine göre “Çizimi Başlat” butonuna basılır. “Komut İçeriği” kısmında verilen komut dosyası görüntülenir. “Loglar” kısmında eğer hata var ise hatanın açıklaması, yoksa RobArt’ın yapacağı işlemler detaylıca yazdırılır. Kullanıcı çizim sırasında “Çizimi Durdur” butonunu kullanarak RobArt’ı durdurabilir, Çizim Hızı ve Çizim Büyüklüğü seçenekleriyle çizim hızını ve büyüklüğünü ayarlayabilir. Bu sonuçlara göre Robart’ın çizimi sağ taraftaki Tuvalde görüntülenir.

    """
    t1.insert(END, syf_1)
    t1.configure(state=DISABLED)

    t2 = Text(frame1,width=70,height=39,bg='#656565',fg='white',border=0,font=('Helvetica',11))
    t2.place(x=597,y=42)

    syf_2="""
    User Guide:
1.1  What does our program do?
1.2  Commands
1.3  Errors
1.4  Programme Settings
1.5  Running the Program 

1.1 What does our program do?

   It draws the desired shape in line with the commands it receives from the user.

1.2 Commands
  
   F : The letter F indicates how many steps forward to draw. Next to F, the number of steps to be drawn in the forward direction should be written.

Example : F 42  -> RobARt 	will draw 42 steps forward
.
   R The letter R indicates how many degrees our RobArt will turn to the right. The number of degrees to be rotated should be written next to R.

Example : R 61  -> RobArt will rotate 61 degrees to the right
.

   L : The letter L symbolizes the cycle. Specifies the number of times to repeat the commands enclosed in square brackets.

Example: L 27 [F 5 R9] -> RobArt will move 5 steps and turn 9 degrees to the right 27 times.


   COLOR : The word COLOR indicates which color RobArt's pen will pick up.
          RobArt has 4 color pencils. These are as follows:
	           K -> Red
	           Y -> Green
	           M -> Blue
	           S -> Black

Example : COLOR M -> RobArt will select the blue pen.



   PEN : The word Pen determines the thickness of RobArt's pen. RobArt has 3 d
   ifferent thicknesses of pens. These are as follows:
	1 -> Thin
	2 -> Normal
	3 -> Thick

Example: PEN 3 -> RobArt will select the thick pen.


1.3 Errors

   - RobArt enlarges any expression that can be entered in lowercase.

   - Unidentified Character: The given script contains a character that RobArt does not recognize.

   - Grammar Error: A syntax error is received when there is a use other than the above command in the given script.

   - Thickness Error: A thickness error is received when a thickness is selected other than the above thicknesses in the given script.

   - Out of Border Error: The drawing that is intended to be drawn with the help of the commands in the script does not fit on the Canvas.

1.4 Program Setting

   - Speed of Drawing: The speed of the drawing to be drawn with RobArt is adjusted.

   - Size of Drawing: The size of the drawing to be drawn with RobArt is adjusted.

   - Try to fix possible errors: RobArt will destroy any unidentified characters if this option is selected.


1.5 Running The Programme

  After the program is opened, the script to be drawn is selected with the "Select" button. Then, the "Start Drawing" button is pressed according to the request to eliminate possible errors. The script given in the “Command Content” section is displayed. In the "Logs" section, if there is an error, the description of the error and the actions to be taken by RobArt are printed in detail. While drawing, the user can stop RobArt by using the "Stop Drawing" button, and adjust the drawing speed and size with the Drawing Speed and Drawing Size options. Based on these results, Robart's drawing is displayed on the Canvas on the right.
    
    """
    t2.insert(END, syf_2)
    t2.configure(state=DISABLED)

    # t2 = Text(frame1,width=70,height=42,border=0)
    # t2.place(x=597,y=42)

    # syf_2 ="""
 
    # """
    # t2.insert(END,syf_2)
    # k_kilavuz.configure(state=NORMAL)




k_kilavuz=CTkButton(sola_kisim,width=150,text= "Kullanım Kılavuzu",text_font=("Helvetica",-15),command=sayfa_ac)
k_kilavuz.place(x=114, y=255)

### Emeği Geçenler ###
def emek():
    ressam.clear()
    ressam.penup()
    ressam.goto(-420,-75)
    ressam.pendown()
    ressam.write("""
       MUSTAFA YILMAZ - 394778

       ISMAIL UCURAN - 394810

       IRMAK SILAY KARA - 402497
    """, font=('Helvetica',30, 'normal'))


b_emek=CTkButton(sola_kisim,width=150, text="Emeği Geçenler",command=emek,text_font=("Helvetica",-15))
b_emek.place(x=274, y=255)

### Dil Seçeneği ###


def change():
    if dil.get()==1:
        komut.configure(text='Select the command file',width=18)
        cizim_hiz.configure(text='Speed of Drawing',width=15)
        cizim_oran.configure(text='Size of Drawing', width=13)
        olasi_hata.configure(text='Try to fix possible errors')
        txt_icerik.configure(text='Command File Content',width=18)
        log.configure(text='Logs',width=5)
        secim.configure(text='Select')
        k_kilavuz.configure(text='User Guide')
        durdur_surdur.configure(text='Stop Drawing')
        baslat.configure(text='Start Drawing')
        b_emek.configure(text='Laborers')
    else:
        komut.configure(text='Komut dosyasını seçiniz',width=18)
        cizim_hiz.configure(text='Çizim Hızı', width=8)
        cizim_oran.configure(text='Çizim Büyüklüğü', width=13)
        olasi_hata.configure(text='Olası hatalar gidelirmeye çalışılsın',width=26)
        txt_icerik.configure(text='Komut Dosyası İçeriği',width=17)
        log.configure(text='Loglar',width=6)
        secim.configure(text='Seç')
        k_kilavuz.configure(text='Kullanım Kılavuzu')
        durdur_surdur.configure(text='Çizimi Durdur')
        baslat.configure(text='Çizimi Başlat')
        b_emek.configure(text='Emeği geçenler')



dil = CTkSwitch(sola_kisim,command = change,text='TR/ENG',text_font=('Helvetica',-10),onvalue=1,offvalue=0,button_color='#11B384',)
dil.place(x=8,y=275)


### Turtle Oluşturma ###
c = Canvas(sag_kisim, width=746.25, height=742.5)
c.pack()

if komutlar.is_error != True:
    screen = turtle.TurtleScreen(c)
    screen.bgcolor('#959595')
    ressam = turtle.RawTurtle(screen)
    ressam.hideturtle()
else:
    print("Verilen Komutlar Hatalı")


ekran.mainloop()
