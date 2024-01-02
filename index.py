import pymysql
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import tkinter as tk

#koneksi untuk phpmyadmin
def connection():
    conn = pymysql.connect(
        host='localhost', user='root', password='', db='siswa'
    )
    return conn

def refreshTable():
    for data in my_tree.get_children():
        my_tree.delete(data)

    for array in read():
        my_tree.insert(parent='', index='end', iid=array, text="", values=(array), tag="orow")

    my_tree.tag_configure('orow', background='#EEEEEE', font=('Arial', 12))
    my_tree.grid(row=8, column=0, columnspan=5, rowspan=11, padx=10, pady=20)

root = Tk()
root.title("Sistem Registrasi Siswa | Mahasiswa")
root.geometry("1080x720")
my_tree = ttk.Treeview(root)

#placeholder untuk masuk
ph1 = tk.StringVar()
ph2 = tk.StringVar()
ph3 = tk.StringVar()
ph4 = tk.StringVar()
ph5 = tk.StringVar()

#placeholder menetapkan fungsi nilai
def setph(word,num):
    if num ==1:
        ph1.set(word)
    if num ==2:
        ph2.set(word)
    if num ==3:
        ph3.set(word)
    if num ==4:
        ph4.set(word)
    if num ==5:
        ph5.set(word)

def read():
    conn = connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM mhs")
    results = cursor.fetchall()
    conn.commit()
    conn.close()
    return results

def tambah():
    Id_Siswa = str(Id_SiswaEntry.get())
    Nama1 = str(Nama1Entry.get())
    Nama2 = str(Nama2Entry.get())
    Alamat = str(AlamatEntry.get())
    No_Hp = str(No_HpEntry.get())

    if (Id_Siswa == "" or Id_Siswa == " ") or (Nama1 == "" or Nama1 == " ") or (Nama2 == "" or Nama2 == " ") or (Alamat == "" or Alamat == " ") or (No_Hp == "" or No_Hp == " "):
        messagebox.showinfo("Eror", "Data Tidak Boleh Kosong !")
        return
    else:
        try:
            conn = connection()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO mhs VALUES (%s, %s, %s, %s, %s)", (Id_Siswa, Nama1, Nama2, Alamat, No_Hp))
            conn.commit()
            conn.close()
        except:
            messagebox.showinfo("Error", "Id Siswa Sudah Terdaftar !")
            return

    refreshTable()
    

def hapussemua():
    decision = messagebox.askquestion("Perhatikan !!", "Anda Yakin Ingin Menghapus Semua Data ?")
    if decision != "yes":
        return 
    else:
        try:
            conn = connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM mhs")
            conn.commit()
            conn.close()
        except:
            messagebox.showinfo("Error", "Terjadi Kesalahan !")
            return

        refreshTable()

def hapus():
    decision = messagebox.askquestion("Peringatan !!", "Anda Ingin MengHapus data yang dipilih ?")
    if decision != "yes":
        return 
    else:
        selected_item = my_tree.selection()[0]
        deleteData = str(my_tree.item(selected_item)['values'][0])
        try:
            conn = connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM mhs WHERE Id_Siswa='"+str(deleteData)+"'")
            conn.commit()
            conn.close()
        except:
            messagebox.showinfo("Error", "Terjadi Kesalahan")
            return

        refreshTable()

def pilih():
    try:
        selected_item = my_tree.selection()[0]
        Id_Siswa = str(my_tree.item(selected_item)['values'][0])
        Nama1 = str(my_tree.item(selected_item)['values'][1])
        Nama2 = str(my_tree.item(selected_item)['values'][2])
        Alamat = str(my_tree.item(selected_item)['values'][3])
        No_Hp = str(my_tree.item(selected_item)['values'][4])

        setph(Id_Siswa,1)
        setph(Nama1,2)
        setph(Nama2,3)
        setph(Alamat,4)
        setph(No_Hp,5)
    except:
        messagebox.showinfo("Error", "Silakan Pilih Data Sesuai Baris Pada Tampilan Data !")

def cari():
    Id_Siswa = str(Id_SiswaEntry.get())
    Nama1 = str(Nama1Entry.get())
    Nama2 = str(Nama2Entry.get())
    Alamat = str(AlamatEntry.get())
    No_Hp = str(No_HpEntry.get())

    conn = connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM mhs WHERE Id_Siswa='"+
    Id_Siswa+"' or Nama1='"+
    Nama1+"' or Nama2='"+
    Nama2+"' or Alamat='"+
    Alamat+"' or No_Hp='"+
    No_Hp+"' ")
    
    try:
        result = cursor.fetchall()

        for num in range(0,5):
            setph(result[0][num],(num+1))

        conn.commit()
        conn.close()
    except:
        messagebox.showinfo("Error", "Data Yang Anda Cari Tidak Ditemukan")

def ubah():
    selectedId_Siswa = ""

    try:
        selected_item = my_tree.selection()[0]
        selectedId_Siswa = str(my_tree.item(selected_item)['values'][0])
    except:
        messagebox.showinfo("Error", "Silakan Pilih/Klik Data Yang Ingin Anda Ubah Pada Tampilan Data !")

    Id_Siswa = str(Id_SiswaEntry.get())
    Nama1 = str(Nama1Entry.get())
    Nama2 = str(Nama2Entry.get())
    Alamat = str(AlamatEntry.get())
    No_Hp = str(No_HpEntry.get())

    if (Id_Siswa == "" or Id_Siswa == " ") or (Nama1 == "" or Nama1 == " ") or (Nama2 == "" or Nama2 == " ") or (Alamat == "" or Alamat == " ") or (No_Hp == "" or No_Hp == " "):
        messagebox.showinfo("Error", "Silakan Isi Kolom Data Masih Kosong !")
        return
    else:
        try:
            conn = connection()
            cursor = conn.cursor()
            cursor.execute("UPDATE mhs SET Id_Siswa='"+
            Id_Siswa+"', Nama1='"+
            Nama1+"', Nama2='"+
            Nama2+"', Alamat='"+
            Alamat+"', No_Hp='"+
            No_Hp+"' WHERE Id_Siswa='"+
            selectedId_Siswa+"' ")
            conn.commit()
            conn.close()
        except:
            messagebox.showinfo("Error", "Id Siswa Ini Sudah Terdaftar")
            return

    refreshTable()

label = Label(root, text="Pendaftaran Siswa | Mahasiswa", font=('Arial Bold', 30))
label.grid(row=0, column=0, columnspan=8, rowspan=2, padx=50, pady=40)

Id_SiswaLabel = Label(root, text="Id Siswa", font=('Arial', 15))
Nama1Label = Label(root, text="Nama Depan", font=('Arial', 15))
Nama2Label = Label(root, text="Nama Belakang", font=('Arial', 15))
AlamatLabel = Label(root, text="Alamat", font=('Arial', 15))
No_HpLabel = Label(root, text="No.Hp", font=('Arial', 15))

Id_SiswaLabel.grid(row=3, column=0, columnspan=1, padx=50, pady=5)
Nama1Label.grid(row=4, column=0, columnspan=1, padx=50, pady=5)
Nama2Label.grid(row=5, column=0, columnspan=1, padx=50, pady=5)
AlamatLabel.grid(row=6, column=0, columnspan=1, padx=50, pady=5)
No_HpLabel.grid(row=7, column=0, columnspan=1, padx=50, pady=5)

Id_SiswaEntry = Entry(root, width=55, bd=5, font=('Arial', 15), textvariable = ph1)
Nama1Entry = Entry(root, width=55, bd=5, font=('Arial', 15), textvariable = ph2)
Nama2Entry = Entry(root, width=55, bd=5, font=('Arial', 15), textvariable = ph3)
AlamatEntry = Entry(root, width=55, bd=5, font=('Arial', 15), textvariable = ph4)
No_HpEntry = Entry(root, width=55, bd=5, font=('Arial', 15), textvariable = ph5)

Id_SiswaEntry.grid(row=3, column=1, columnspan=4, padx=5, pady=0)
Nama1Entry.grid(row=4, column=1, columnspan=4, padx=5, pady=0)
Nama2Entry.grid(row=5, column=1, columnspan=4, padx=5, pady=0)
AlamatEntry.grid(row=6, column=1, columnspan=4, padx=5, pady=0)
No_HpEntry.grid(row=7, column=1, columnspan=4, padx=5, pady=0)

addBtn = Button(
    root, text="Tambah", padx=45, pady=7, width=8,
    bd=5, font=('Arial', 15), bg="#84F894", command=tambah)
updateBtn = Button(
    root, text="Ubah", padx=45, pady=7, width=8,
    bd=5, font=('Arial', 15), bg="#84E8F8", command=ubah)
deleteBtn = Button(
    root, text="Hapus", padx=45, pady=7, width=8,
    bd=5, font=('Arial', 15), bg="#FF9999", command=hapus)
searchBtn = Button(
    root, text="Cari", padx=45, pady=7, width=8,
    bd=5, font=('Arial', 15), bg="#F4FE82", command=cari)
resetBtn = Button(
    root, text="Hapus Semua", padx=45, pady=7, width=8,
    bd=5, font=('Arial', 15), bg="#F398FF", command=hapussemua)
selectBtn = Button(
    root, text="Pilih", padx=45, pady=7, width=8,
    bd=5, font=('Arial', 15), bg="#EEEEEE", command=pilih)

addBtn.grid(row=3, column=5, columnspan=1, rowspan=2)
updateBtn.grid(row=5, column=5, columnspan=1, rowspan=2)
deleteBtn.grid(row=7, column=5, columnspan=1, rowspan=2)
searchBtn.grid(row=9, column=5, columnspan=1, rowspan=2)
resetBtn.grid(row=11, column=5, columnspan=1, rowspan=2)
selectBtn.grid(row=13, column=5, columnspan=1, rowspan=2)

style = ttk.Style()
style.configure("Treeview.Heading", font=('Arial Bold', 15))

my_tree['columns'] = ("Id Siswa","Nama Depan","Nama Belakang","Alamat","Nomor HP")

my_tree.column("#0", width=0, stretch=NO)
my_tree.column("Id Siswa", anchor=W, width=170)
my_tree.column("Nama Depan", anchor=W, width=150)
my_tree.column("Nama Belakang", anchor=W, width=150)
my_tree.column("Alamat", anchor=W, width=165)
my_tree.column("Nomor HP", anchor=W, width=150)


my_tree.heading("Id Siswa", text="Id Siswa", anchor=W)
my_tree.heading("Nama Depan", text="NamaDepan", anchor=W)
my_tree.heading("Nama Belakang", text="NamaBelakang", anchor=W)
my_tree.heading("Alamat", text="Alamat", anchor=W)
my_tree.heading("Nomor HP", text="No.HP", anchor=W)

refreshTable()

root.mainloop()