from win32com.client import DispatchEx
import pywintypes
import time
from bs4 import BeautifulSoup
import datetime
import tkinter as tk
from tkinter import messagebox
from pygame import mixer
import threading, os

mixer.init()

def cek_waktu():
    global pray_time_today, pray_table, coba, pray_time_today_dt, nama_tk, waktu_tk, tg
    ie = DispatchEx('InternetExplorer.Application')
    ie.Visible = 0
    ie.Navigate("https://jadwalsholat.pkpu.or.id/?id=308")

    coba = 0
    def coba_ie():
        global myfilebox, coba
        try:
            myfile = open('data.html', 'r')
            myfilebox = myfile.read()
            myfile.close()
            soup = BeautifulSoup(myfilebox,"html.parser")
            databulan = soup.find_all('td', {"style":"width: 50%;"})
            databulan = databulan[0].find_all('b')[0].contents[0]
            databulanskr = datetime.datetime.now()
            databulanskr = datetime.datetime.strftime(databulanskr, "%B %Y")
            bulan_id = {
                'January':'Januari',
                'February':'Februari',
                'March' : 'Maret',
                'April' : 'April',
                'May' : 'Mei',
                'Juny' : 'Juni',
                'July' : 'Juli',
                'August' : 'Agustus',
                'September' : 'September',
                'October' : 'Oktober',
                'November' : 'November',
                'December' : 'Desember'
                }
            databulanskr = databulanskr.split(' ')
            databulanskr[0] = bulan_id[databulanskr[0]]
            databulanskr = ' '.join(databulanskr)
            if databulan == databulanskr:
                return
            else:
                os.remove('data.html')
                myfile = open('data.html', 'r')
        except FileNotFoundError:
            try:
                myfilebox = ie.Document.body.innerHTML
                myfile = open('data.html', 'w')
                myfile.write(myfilebox)
                myfile.close()
            except pywintypes.com_error:
                time.sleep(3)
                coba += 1
                if coba <= 5:
                    coba_ie()
                else:
                    try:
                        myfile = open('data.html')
                        myfilebox = myfile.read()
                        myfile.close()
                    except FileNotFoundError:                       
                        messagebox.showinfo('Error','Minimal 1x ada koneksi')
                        root.destroy()
                        tg = 1
                        return        

                
    coba_ie()
   
    ie.Quit()

    soup = BeautifulSoup(myfilebox,"html.parser")
    tables = soup.find_all('tr', {"align": "center"})
    day = datetime.datetime.now().day

    pray_table = tables[day].findAll("td")
    pray_time_today = {}
    pray_time_today_dt = {}
    waktu_skr  = datetime.datetime.now()
    tahun = waktu_skr.year
    bulan = waktu_skr.month
    tanggal = waktu_skr.day   
    
    shalat_name = ['Tgl', 'Shubuh', 'Dzuhur', 'Ashr', 'Maghrib', 'Isya']

    for n in range(1, len(pray_table)):
        pray_time_today[shalat_name[n]] = str(pray_table[n].contents[0])
        time_shalat = datetime.datetime.strptime(pray_time_today[shalat_name[n]], "%H:%M")
        jam = time_shalat.hour
        menit = time_shalat.minute
        pray_time_today_dt[shalat_name[n]] = datetime.datetime(tahun, bulan, tanggal, jam, menit)

    nama_tk = {}
    waktu_tk = {}

    n = 0
    for nama in pray_time_today:
        nama_tk[nama] = tk.Label(frame_nama, text=nama, bg='lightblue', padx = 20)
        nama_tk[nama].grid(row=n, column=0)
        waktu_tk[nama] = tk.Label(frame_nama, text=pray_time_today[nama], padx = 20, bg='white')
        waktu_tk[nama].grid(row=n, column=1)
        n += 1

def ontop():
    global ontop
    if ontop == 0:
        root.attributes("-topmost", True)
        filemenu.entryconfigure(0, label="Always on Top \u2713")
        root.attributes("-alpha", .70)
        ontop = 1
    else:
        root.attributes("-topmost", False)
        filemenu.entryconfigure(0, label="Always on Top")
        root.attributes("-alpha", 1)
        ontop = 0

def opensite():
    os.startfile('https://jadwalsholat.pkpu.or.id/?id=308')

def threadmain():
    global root, frame_nama, waktu_skr, stop_button, filemenu
       
    waktu_skr  = datetime.datetime.now()     
    root = tk.Tk()
    icon = resource_path("praying-icon.ico")
    root.iconbitmap(icon) 
    root.resizable(width=False, height=False)
    root.title('Waktu Shalat')
    frame_nama = tk.Frame(root, bg='lightblue')
    frame_nama.grid(row=0, column=0)
    frame_button = tk.Frame(root)
    frame_button.grid(row=1, column=0, columnspan = 2)
    stop_button = tk.Button(frame_button, text='Stop Sound', command=stopazan)
    stop_button.pack()
    stop_button.configure(state='disabled')
    menu = tk.Menu(root)
    root.config(menu=menu)
    filemenu = tk.Menu(menu, tearoff=0)
    menu.add_cascade(label="Help", menu=filemenu)
    filemenu.add_command(label="Always on Top", command=ontop)
    filemenu.add_command(label="Open Shalat site", command=opensite)
    filemenu.add_command(label="Exit", command=onexit)
    root.protocol("WM_DELETE_WINDOW", onexit)
    root.after(1000, cek_time_shalat)
    root.mainloop()

def onexit():
        global tg
        tg = 1

def cek_time_shalat():
    global shalat_selanjut, warna, shalat_sekarang
    waktu_skr  = datetime.datetime.now()

    try:
        for waktu in pray_time_today_dt:
            if pray_time_today_dt[waktu] < waktu_skr:
                shalat_sekarang = waktu
                warna = 'light'
                if shalat_sekarang == 'Isya':
                    shalat_selanjut = 'Shubuh'
                    root.after(3000, highlight)
                    break
                
            if pray_time_today_dt[waktu] > waktu_skr:
                shalat_selanjut = waktu                
                waktu_tk[shalat_selanjut].config(bg='blue', fg='white')
                root.after(3000, highlight)
                break
               
    except NameError:
        root.after(1000, cek_time_shalat)

def waktu_shalat():
    if shalat_sekarang == 'Shubuh':
        mixer.music.load(azansubuh)
    else:
        mixer.music.load(azan)
    mixer.music.play()
    stop_button.configure(state='normal')
    os.startfile(salatpng)
    root.after(1000, cek_time_shalat)

def stopazan():
    mixer.music.stop()
    stop_button.configure(state='disabled')
        
def highlight():
    global warna
    
    waktu_skr  = datetime.datetime.now()
    waktu_nanti = pray_time_today_dt[shalat_selanjut]
    jarak_30min = waktu_skr + datetime.timedelta(minutes = 30)
           
    if waktu_skr >= waktu_nanti:
        waktu_tk[shalat_sekarang].config(bg='white', fg='black')
        waktu_shalat()
        return

    if jarak_30min < waktu_nanti:
        if warna == 'light':
            waktu_tk[shalat_sekarang].config(bg='green', fg='white')
            warna = 'dark'
        elif warna == 'dark':
            waktu_tk[shalat_sekarang].config(bg='light green', fg='black')
            warna = 'light'

        root.after(3000, highlight)
    else:
        waktu_tk[shalat_selanjut].config(bg='green', fg='white')
        if warna == 'light':
            waktu_tk[shalat_sekarang].config(bg='red', fg='white')
            warna = 'dark'
        elif warna == 'dark':
            waktu_tk[shalat_sekarang].config(bg='yellow', fg='black')
            warna = 'light'
        root.after(3000, highlight)
    if shalat_sekarang == 'Shubuh' and pray_time_today_dt[shalat_sekarang]+datetime.timedelta(minutes = 30) < waktu_skr:
        waktu_tk[shalat_sekarang].config(bg='white', fg='black')

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

azansubuh = resource_path('azansubuh.mp3')
azan = resource_path('azan.mp3')
salatpng = resource_path('shalat.png')
        
if __name__ == '__main__':
    st = threading.Thread(target=threadmain)
    st.daemon = True
    st.start()
    cek_waktu()
    tg = 0
    ontop = 0
    while 1:
        if tg == 1:
            root.quit()
            break
