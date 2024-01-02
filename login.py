import mysql.connector
import pymysql
import os
from tkinter import *
from tkinter import ttk
import tkinter as tk

def connect_to_database():
    # Ganti informasi koneksi sesuai dengan database Anda
    db_config = {
        'host': 'localhost',
        'user': 'root',
        'password': '',
        'database': 'login'
    }

    try:
        connection = mysql.connector.connect(**db_config)
        if connection.is_connected():
            return connection
    except mysql.connector.Error as err:
        print(f'Error: {err}')
        return None
    
def on_login_success(root):
    root.destroy()    
    # Menjalankan file home.py
    os.system("python home.py")

def login(username, password, label_result, root, frame_login, frame_registration):
    # Terhubung ke database
    connection = connect_to_database()

    if connection:
        try:
            # Misalnya, membuat kursor dan menjalankan query
            cursor = connection.cursor()

            # Query untuk memeriksa apakah kombinasi email dan password sesuai
            query = "SELECT * FROM log WHERE email = %s AND password = %s"
            cursor.execute(query, (username, password))
            result = cursor.fetchone()

            if result:
                # Jika data ditemukan, tampilkan pesan login berhasil
                label_result.config(text='Login berhasil.', fg='green')
                # Menutup koneksi
                cursor.close()
                connection.close()
                # Beralih ke halaman home.py setelah login berhasil
                on_login_success(root)
                return
            else:
                # Jika data tidak ditemukan, tampilkan pesan akun belum terdaftar
                label_result.config(text='Akun email belum terdaftar.', fg='red')

        except pymysql.Error as err:
            # Jika terjadi kesalahan dalam eksekusi query
            label_result.config(text=f'Error: {err}', fg='red')

        finally:
            # Menutup koneksi di blok finally untuk memastikan koneksi ditutup
            cursor.close()
            connection.close()


def switch_to_registration(frame_login, frame_registration):
    # Menampilkan halaman registrasi dan menyembunyikan halaman login
    frame_login.pack_forget()
    frame_registration.pack()

def simpan_data_login(username, password, label_result, frame_login, frame_registration):
    # Terhubung ke database
    connection = connect_to_database()

    if connection:
        try:
            # Misalnya, membuat kursor dan menjalankan query
            cursor = connection.cursor()

            # Query untuk menyimpan data login ke dalam tabel
            query = "INSERT INTO log (email, password) VALUES (%s, %s)"
            cursor.execute(query, (username, password))

            # Commit perubahan ke database
            connection.commit()

            label_result.config(text='Registrasi berhasil. Data login disimpan.', fg='green')

            # Menyembunyikan frame registrasi dan menampilkan frame login
            frame_registration.pack_forget()
            frame_login.pack()

        except mysql.connector.Error as err:
            # Jika terjadi kesalahan, rollback perubahan
            connection.rollback()
            label_result.config(text=f'Error: {err}', fg='red')

        finally:
            # Menutup koneksi
            cursor.close()
            connection.close()

def registrasi(entry_username, entry_password, label_result, frame_login, frame_registration):
    # Memasukkan email dan password baru dari pengguna
    new_username = entry_username.get()
    new_password = entry_password.get()

    # Menyimpan data registrasi ke dalam database
    simpan_data_login(new_username, new_password, label_result, frame_login, frame_registration)


def main():
    root = tk.Tk()
    root.title("Login GUI")
    root.geometry("400x300")  # Mengatur ukuran jendela

    # Frame untuk halaman login
    frame_login = tk.Frame(root, bg='lightblue')  # Warna latar belakang
    frame_login.pack()

    label_username = tk.Label(frame_login, text="Email:", bg='lightblue')  # Warna latar belakang
    label_username.pack()
    entry_username = tk.Entry(frame_login)
    entry_username.pack()

    label_password = tk.Label(frame_login, text="Password:", bg='lightblue')  # Warna latar belakang
    label_password.pack()
    entry_password = tk.Entry(frame_login, show="*")
    entry_password.pack()

    label_result = tk.Label(frame_login, text="", fg='red')  # Warna teks
    label_result.pack()

    button_login = tk.Button(frame_login, text="Login", command=lambda: login(entry_username.get(), entry_password.get(), label_result, root, frame_login, frame_registration), bg='green', fg='white')  # Warna tombol
    button_login.pack()

    label_not_registered = tk.Label(frame_login, text="Belum Punya Akun?", bg='lightblue')  # Warna latar belakang
    label_not_registered.pack()

    button_switch_to_registration = tk.Button(frame_login, text="Daftar", command=lambda: switch_to_registration(frame_login, frame_registration), bg='blue', fg='white')  # Warna tombol
    button_switch_to_registration.pack()

    # Frame untuk halaman registrasi
    frame_registration = tk.Frame(root, bg='lightgreen')  # Warna latar belakang
    frame_registration.pack()

    label_new_username = tk.Label(frame_registration, text="Masukkan email baru:", bg='lightgreen')  # Warna latar belakang
    label_new_username.pack()
    entry_new_username = tk.Entry(frame_registration)
    entry_new_username.pack()

    label_new_password = tk.Label(frame_registration, text="Masukkan password baru:", bg='lightgreen')  # Warna latar belakang
    label_new_password.pack()
    entry_new_password = tk.Entry(frame_registration, show="*")
    entry_new_password.pack()

    label_registration_result = tk.Label(frame_registration, text="", fg='red')  # Warna teks
    label_registration_result.pack()

    button_register = tk.Button(frame_registration, text="Registrasi", command=lambda: registrasi(entry_new_username, entry_new_password, label_registration_result, frame_login, frame_registration), bg='green', fg='white')  # Warna tombol
    button_register.pack()

    # Menyembunyikan frame registrasi
    frame_registration.pack_forget()

    root.mainloop()

if __name__ == "__main__":
    main()
