##import webbrowser, os, bs4, re, time, pyautogui, win32gui, tkinter, datetime
import webbrowser, os, bs4, re, time, pyautogui, tkinter, datetime, requests, socket
from tkinter import messagebox
from pygame import mixer

address = 'http://jadwalsholat.pkpu.or.id/monthly.php?id=308'
folder = r'D:\Users\Downloads'
file = ''
filepath = os.path.join(folder, file)

##web =  requests.get(address)
##web.raise_for_status()
##webtext = bs4.BeautifulSoup(web.text)

p = 0
e = 0
test = ""
##def moving():
##        global test
##        time.sleep(2)
##        test = win32gui.FindWindow(None, "Waktu Shalat Gan")
##        if test > 0:
##                x,y,wi,he = win32gui.GetWindowRect(test)
##                wi = wi-x
##                he = he-y
##                win32gui.MoveWindow(test, 1000, 450, wi, he, False)
##                win32gui.SetForegroundWindow(test)
##        else:
##                moving()



def cekrefresh():
        try:
                messagebox.showinfo("Checking", "checking internet connection..")
                socket.setdefaulttimeout(15)
                host = socket.gethostbyname("www.google.com")
                s = socket.create_connection((host, 80), 2)
                s.close()
                return 1
        except Exception:
                return 0

def solat():
##    os.system('cls')
        global p, w, e, cc, c, file, b, a
        internet = cekrefresh()
        if internet == 1:
                web =  requests.get(address)
                webtext = bs4.BeautifulSoup(web.text, 'html.parser')
                a = webtext.select("tr[align='center']")
                a = str(a[0])
                openfile = open('jadwalshalat.txt', 'w')
                openfile.write(a)
                openfile.close()
                openfile = open('jadwalshalat.txt')
                a = openfile.read()
        else:
                messagebox.showinfo('Ga ada koneksi internet', 'cek manual dari file')
                try:
                        for filename in os.listdir():
                                if filename.endswith('.html'):
                                        file = filename
                                        break
                        print(file)
                        openfile = open(file)
                        opensoup = bs4.BeautifulSoup(openfile, 'html.parser')
                        a = opensoup.select("tr[align='center']")
##                        a = str(a[0])
                        a = str(a)
                        openfile = open('jadwalshalat.txt', 'w')
                        openfile.write(a)
                        openfile.close()
                        openfile = open('jadwalshalat.txt')
                        a = openfile.read()
                        openfile.close()

                except FileNotFoundError:
                        messagebox.showinfo('error', 'manual update file ga ada,  jadinya pake data lama')
                        try:
                                openfile = open('jadwalshalat.txt')
                                a = openfile.read()                    
                        except FileNotFoundError:
                                messagebox.showinfo('Data lama ga ada', 'Please activate your internet or put file : ' + file + ' in same folder')
                                return
##        
        datenow = datetime.datetime.now()
        datenow = datenow.strftime('%d')
        b = re.compile(r'<b>'+datenow+'</b></td><td>(\d\d:\d\d)</td><td>(\d\d:\d\d)</td><td>(\d\d:\d\d)</td><td>(\d\d:\d\d)</td><td>(\d\d:\d\d)')
        c = b.findall(a)
        c = c[0]
        if p == 0:         
                p = 1
                rr = 0
                for i in d:
                    w[e] = tkinter.Label(root,
                                        text=c[e],
                                        padx = 20,
                                        justify='left', bg="white")
                    w[e].grid(row=rr, column=1)
                    e += 1
                    rr += 1
                cektime()
        else:
##                webbrowser.open(address)
##                time.sleep(2)
##                pyautogui.hotkey('ctrl', 's')
##                time.sleep(2)
##                pyautogui.hotkey('ctrl', 'c')
##                pyautogui.typewrite(['tab','w','w', 'enter', 'y'])
##                time.sleep(2)
##                try:
##                        openfile = open(filepath)
##                except FileNotFoundError:
##                        openfile = open(file)
##                opensoup = bs4.BeautifulSoup(openfile, 'html.parser')
##                a = opensoup.select("tr[class='table_highlight']")
##                a = str(a[0])
##                b = re.compile(r'\d\d:\d\d')
##                c = b.findall(a)
                e = 0
                for i in d:
                    w[e].configure(text=c[e])
                    e += 1
                cektime()
##                moving()

gantiaku = 0
nil = 0
gambar = 0
sama = 0
def cektime():
        global s,gantiaku, notext, now, time1, timenow, nil,sa, gambar, sama
        now = datetime.datetime.now()
        notext = now.strftime('%H:%M')
        timenow = now.replace(hour=int(notext[0:2]), minute=int(notext[3:6]), second=0, microsecond=0)
        for i in range(5):
                time1 = now.replace(hour=int(c[i][0:2]), minute=int(c[i][3:6]), second=0, microsecond=0)
                if time1 == timenow:
                        if sama == 0:
                                sama = 1
                                if gambar == 0:
                                        gambar = 1
                                        sop.configure(state='normal')
                                        if str(d[i]) == 'Shubuh':
                                               mixer.music.load('azansubuh.mp3')
                                               mixer.music.play()
                                        else:
                                               mixer.music.load('azan.mp3')
                                               mixer.music.play()
                                        os.startfile('shalat.png')
##                                        messagebox.showinfo('Waktu Shalat', 'Waktu shalat '+str(d[i]) +' gan!')
                        sa = i
                        if i == 4:
                                sa = 0
                        else:
                                sa+=1
                        w[sa].configure(bg='blue', fg='white')
                        s = i
                        minus30()
                        ganti()
                        nil = 0                                
                        break

                elif time1 > timenow:
                        w[i].configure(bg='blue', fg='white')
                        sa = i
                        if i > 0:
                                s = sa-1
                        else:
                                s = 4
                        w[s].configure(bg='light green')
                        
                        minus30()
                        ganti()
                        nil = 0
                        
                        break
                else:
                        if nil < 5:
                                nil +=1
                        elif nil == 5:
                                sa = 0
                                s = 4
                                w[sa].configure(bg='blue', fg='white')
                                nil = 0
                                minus30()
                                ganti()
                        
        root.after(2000, cektime)
        
def minus30():
        global min30, other, bal                
        da = now.day
        other = []
       
        if s == 4 or sa == 0:
                bal = [0, 4]
        else:
                bal = [s, sa]
        for i in range(5):
                if i not in bal:
                        other += [i]                
        if s != 4:
                jams = int(c[s+1][0:2])
                menits = int(c[s+1][3:6])
        else:
                jams = int(c[0][0:2])
                menits = int(c[0][3:6])
                da += 1
        for i in other:
                w[i].configure(bg='white', fg='black')
        if menits < 30:
               if jams < 1:
                       jams = 0
               if jams >= 1 :
                       jams -= 1
                       menits += 60
        if menits > 30:
               min30 = now.replace(day=da, hour=jams, minute=menits-30, second=0, microsecond=0)
        else:
               min30 = now.replace(day=da, hour=jams, minute=menits, second=0, microsecond=0)


noob = 0
plus1 = 0
def ganti():
        global gantiaku, tsubuh, tsubuh30min, sis, gambar, balik, noob, sama, plus1
##        print('sama='+str(sama))
##        print('gambar='+str(gambar))
##        print('noob='+str(noob))
        if gambar == 1:

                if noob == 0:
                        plus1 = s
                        noob = 1
                else:
                        balik = now.replace(hour=int(c[plus1][0:2]), minute=int(c[plus1][3:6])+1, second=0, microsecond=0)
                        if timenow > balik:
                                gambar = 0
                                noob = 0
                                sama = 0
        sis = int(c[0][3:6])
        if sis < 15:
                tsubuh = now.replace(hour=int(c[0][0:2]), minute=int(c[0][3:6])+45, second=0, microsecond=0)
        else:
                sis = sis-15
                tsubuh = now.replace(hour=int(c[0][0:2])+1, minute=sis, second=0, microsecond=0)
        sis = int(c[0][3:6])
        if sis < 30:
                tsubuh30min = now.replace(hour=int(c[0][0:2]), minute=int(c[0][3:6])+30, second=0, microsecond=0)
        else:
                sis = sis-30
                tsubuh30min = now.replace(hour=int(c[0][0:2])+1, minute=sis, second=0, microsecond=0)
        if gantiaku == 0:
                if timenow  < min30:
                        if s == 0 and timenow < tsubuh30min:
                                w[s].configure(bg='light green', fg='black')
                        elif s == 0 and timenow < tsubuh and timenow > tsubuh30min or (s == 0 and timenow > tsubuh):
                                w[s].configure(bg='yellow', fg='black')
                        elif s != 0:
                                w[s].configure(bg='light green', fg='black')
                else:
                        w[s].configure(bg='yellow', fg='black')
                gantiaku = 1
                return
        elif gantiaku == 1:
                if timenow  < min30:
                        if s == 0 and timenow < tsubuh30min:
                                w[s].configure(bg='green', fg='white')
                        elif s == 0 and timenow < tsubuh and timenow > tsubuh30min  or (s == 0 and timenow > tsubuh):
                                w[s].configure(bg='red', fg='white')
                        elif s != 0:
                                w[s].configure(bg='green', fg='white')
                        
                else:
                        w[s].configure(bg='red', fg='white')
                gantiaku = 0
                



root = tkinter.Tk()
root.title("Waktu Shalat Gan")
pat = "praying-icon.ico"
root.iconbitmap(pat) 
root.geometry('{}x{}'.format(150,160))
root.resizable(width=False, height=False)
menu = tkinter.Menu(root)
root.config(menu=menu)
filemenu = tkinter.Menu(menu, tearoff=0)
helpmenu = tkinter.Menu(menu, tearoff=0)
menu.add_cascade(label="Created By Fikri", menu=filemenu)
filemenu.add_command(label="Keluar", command=root.destroy)

button = tkinter.Button(root, text='refresh', command=solat)
button.grid(row=6, column =1, pady=5)

def stopazan():
        mixer.music.stop()
        sop.configure(state='disabled')

sop = tkinter.Button(root, text='Stop Sound', command=stopazan)
sop.grid(row=6, column =0, pady=5)
sop.configure(state='disabled')

d = ['Shubuh', 'Zhuhur', 'Ashar', 'Magrib', 'Isya']
l = {}
w = {}
rr = 0
cc = 0

for i in d:
    l[i] = tkinter.Label(root, 
          text=i,
          bg = "light blue",
          padx = 20)
    l[i].grid(row=rr, column=cc, sticky= 'w'+'e')
    rr += 1

solat()
##moving()
root.after(100, cektime)
mixer.init()

root.mainloop()
