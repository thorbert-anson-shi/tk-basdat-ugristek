from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from django.http import Http404

# Decorator Import
from django.views.decorators.csrf import csrf_exempt

# Database Import
from django.db import connection


# First Landing Page for Auth
def first_auth_page(request):
    # Login and Register Page
    return render(request, "authenticate/login-register.html")

# Login view
def login(request):
    if request.method == "POST":
        
        # Get information from form
        phone = request.POST.get("no_hp")
        password = request.POST.get("password")

        # Check if phone or password is empty
        if not phone or not password:
            error_message = "No HP atau password tidak boleh kosong."
            return render(
                request, "authenticate/login.html", {"error_message": error_message}
            )

        # Doing validation to databases
        with connection.cursor() as c:
            c.execute("SELECT * FROM sijarta.users WHERE nohp = %s AND pwd = %s", [phone, password])
            user = c.fetchone()
            
        if user:
            nama = user[1]  
            # If user found, figure out the role
            user_id = str(user[0])
            
            with connection.cursor() as c:
                c.execute("SELECT * FROM sijarta.pekerja WHERE id = %s", [user_id])
                pekerja = c.fetchone()
                
                c.execute("SELECT * FROM sijarta.pelanggan WHERE id = %s", [user_id])
                pelanggan = c.fetchone()
            
            if pekerja:
                user_session = {
                    "id" : user_id,
                    "no_hp" : phone,
                    "nama" : nama,
                    "saldo" : int(user[7]),
                    "role" : "pekerja"
                }       
            elif pelanggan:
                user_session = {
                    "id" : user_id,
                    "no_hp" : phone,
                    "nama" : nama,
                    "saldo" : int(user[7]),
                    "role" : "pelanggan"
                }      
            
            request.session["user"] = user_session
            
            return redirect("homepage")
            
        else:
            # If user not found
            error_message = "No HP atau password salah"
            return render(
                request, "authenticate/login.html", {"error_message": error_message}
            )

    return render(request, "authenticate/login.html")

# Halaman Logout
def logout(request):
    if "user" in request.session:
        del request.session["user"]  # Hapus sesi pengguna
    return redirect("login")

def register_pelanggan(request):
    
    # If not POST, return the page
    if request.method != "POST":
        return render(request, "authenticate/register_pelanggan.html")
    
    # Get information from form
    nama = request.POST.get("nama")
    password = request.POST.get("password")
    jenis_kelamin = request.POST.get("jenis_kelamin")
    no_hp = request.POST.get("no_hp")
    tanggal_lahir = request.POST.get("tanggal_lahir")
    alamat = request.POST.get("alamat")
    
    # Not sure what this prevent, but just a safety measure
    if not nama or not password or not jenis_kelamin or not no_hp or not tanggal_lahir or not alamat:
        error_message = "Data tidak boleh kosong."
        return render(
            request, "authenticate/register_pelanggan.html", {"error_message": error_message}
        )
        
    print(nama, password, jenis_kelamin, no_hp, tanggal_lahir, alamat)
    # Insert to database
    try:
        with connection.cursor() as c:
            c.execute("INSERT INTO sijarta.users (nama, jeniskelamin, nohp, pwd, tgllahir, alamat, saldomypay) VALUES (%s, %s, %s, %s, %s, %s, %s)", [nama, jenis_kelamin, no_hp, password, tanggal_lahir, alamat, 0])
            c.execute("SELECT id FROM sijarta.users WHERE nohp = %s", [no_hp])
            user_id = str(c.fetchone()[0])
            c.execute("INSERT INTO sijarta.pelanggan (id, level) VALUES (%s, %s)", [user_id, "Basic"])
    except Exception as e:
        print(e)
        error_message = "Nomor HP telah terdaftar."
        return render(
            request, "authenticate/register_pelanggan.html", {"error_message": error_message}
        )
        
    return render(request, "authenticate/login.html")


def register_pekerja(request):
    if request.method != "POST":
        return render(request, "authenticate/register_pekerja.html")

    nama = request.POST.get("nama")
    password = request.POST.get("password")
    jenis_kelamin = request.POST.get("gender")
    no_hp = request.POST.get("phone")
    tanggal_lahir = request.POST.get("birthdate")
    alamat = request.POST.get("address")
    nama_bank = request.POST.get("bank_name")
    no_rek = request.POST.get("bank_account")
    npwp = request.POST.get("npwp")
    url_foto = request.POST.get("photo_url")
    
    c = connection.cursor()
    
    if not nama or not password or not jenis_kelamin or not no_hp or not tanggal_lahir or not alamat or not nama_bank or not no_rek or not npwp or not url_foto:
        error_message = "Data tidak boleh kosong."
        return render(
            request, "authenticate/register_pekerja.html", {"error_message": error_message}
        )

    # Find out if the social security number is unique
    c.execute("SELECT * FROM sijarta.pekerja WHERE nomorrekening = %s and namabank = %s", [no_rek, nama_bank])
    pekerja = c.fetchone()
    
    # Cannt use trigger because the implementation are shitty
    if pekerja:
        error_message = "Nomor Rekening telah terdaftar."
        return render(
            request, "authenticate/register_pekerja.html", {"error_message": error_message}
        )
    
    # Insert to database
    try:
        c.execute("INSERT INTO sijarta.users (nama, jeniskelamin, nohp, pwd, tgllahir, alamat, saldomypay) VALUES (%s, %s, %s, %s, %s, %s, %s)", [nama, jenis_kelamin, no_hp, password, tanggal_lahir, alamat, 0])
        c.execute("SELECT id FROM sijarta.users WHERE nohp = %s", [no_hp])
        user_id = str(c.fetchone()[0])
        c.execute("INSERT INTO sijarta.pekerja (id, namabank, nomorrekening, npwp, linkfoto, rating, jmlpesananselesai) VALUES (%s, %s, %s, %s, %s, %s, %s)", [user_id, nama_bank, no_rek, npwp, url_foto, 0.0, 0])
    except:
        error_message = "Nomor HP telah terdaftar."
        return render(
            request, "authenticate/register_pekerja.html", {"error_message": error_message}
        )
    
    return render(request, "authenticate/login.html")

def register(request):
    return render(request, "authenticate/register.html")

def profile(request):
    # Mendapatkan nomor HP dari session
    user_session = request.session.get("user", None)
    role = user_session.get("role")

    if not user_session:
        raise Http404("User not logged in")  # Pengguna harus login terlebih dahulu
    
    # Get user information
    c = connection.cursor()
    c.execute("SELECT * FROM sijarta.users WHERE id = %s", [user_session["id"]])
    user = c.fetchone()
    
    context = {
        "nama" : user[1],
        "jenis_kelamin" : user[2],
        "no_hp" : user[3],
        "tanggal_lahir" : user[5],
        "alamat" : user[6],
        "saldo" : user[7],
        "role" : role
    }
    
    # Get specifiec information based on role
    if role == "pelanggan":
        c.execute("SELECT * FROM sijarta.pelanggan WHERE id = %s", [user_session["id"]])
        user_pelanggan = c.fetchone()
        context["level"] = user_pelanggan[1]
    
    elif role == "pekerja":
        c.execute("SELECT * FROM sijarta.pekerja WHERE id = %s", [user_session["id"]])
        user_pekerja = c.fetchone()
        
        c.execute("SELECT namakategori FROM sijarta.kategori_jasa kj JOIN sijarta.pekerja_kategori_jasa pkj ON kj.id = pkj.kategorijasaid WHERE pkj.pekerjaid = %s", [user_session["id"]])
        list_kategori = c.fetchall()
        
        list_kategori = [kategori[0].replace(",", "").replace(".", "").strip() for kategori in list_kategori]
        
        context["nama_bank"] = user_pekerja[1]
        context["no_rekening"] = user_pekerja[2]
        context["npwp"] = user_pekerja[3]
        context["url_foto"] = user_pekerja[4]
        context["rating"] = user_pekerja[5]
        context["jml_pesanan_selesai"] = user_pekerja[6]    
        context["list_kategori"] = list_kategori

    return render(request, "profile.html", context)


def updateProfile(request):
    user_session = request.session.get("user", None)
    role = user_session.get("role")
    if not user_session:
        raise Http404("User not logged in")  # Pengguna harus login terlebih dahulu

    if request.method != "POST":
        return render(request, "updateProfile.html", {"role": role})  
    
    c = connection.cursor()

    if role == "pelanggan":
        nama = request.POST.get("nama")
        jenis_kelamin = request.POST.get("jenis_kelamin")
        no_hp = request.POST.get("no_hp")
        tanggal_lahir = request.POST.get("tanggal_lahir")
        alamat = request.POST.get("alamat")
        
        if not nama or not jenis_kelamin or not no_hp or not tanggal_lahir or not alamat:
            error_message = "Data tidak boleh kosong."
            return render(
                request, "updateProfile.html", {"error_message": error_message, "role": role}
            )
        
        try:    
            c.execute("UPDATE sijarta.users SET nama = %s, jeniskelamin = %s, nohp = %s, tgllahir = %s, alamat = %s WHERE id = %s", [nama, jenis_kelamin, no_hp, tanggal_lahir, alamat, user_session["id"]])
            user_session["nama"] = nama
            user_session["no_hp"] = no_hp
        except:
            error_message = "Nomor HP telah terdaftar."
            return render(
                request, "updateProfile.html", {"error_message": error_message, "role": role}
            )
        
        return redirect("profile")
    
    elif role == "pekerja":
        nama = request.POST.get("nama")
        jenis_kelamin = request.POST.get("gender")
        no_hp = request.POST.get("phone")
        tanggal_lahir = request.POST.get("birthdate")
        alamat = request.POST.get("address")
        nama_bank = request.POST.get("bank_name")
        no_rek = request.POST.get("bank_account")
        npwp = request.POST.get("npwp")
        url_foto = request.POST.get("photo_url")
        
        if not nama or not jenis_kelamin or not no_hp or not tanggal_lahir or not alamat or not nama_bank or not no_rek or not npwp or not url_foto:
            error_message = "Data tidak boleh kosong."
            return render(
                request, "updateProfile.html", {"error_message": error_message, "role": role}
            )
        
        # Find out if the social security number is unique
        c.execute("SELECT * FROM sijarta.pekerja WHERE nomorrekening = %s and namabank = %s", [no_rek, nama_bank])
        pekerja = c.fetchone()
        
        if pekerja:
            error_message = "Nomor Rekening telah terdaftar."
            return render(
                request, "updateProfile.html", {"error_message": error_message, "role": role}
            )
        
        try:
            c.execute("UPDATE sijarta.users SET nama = %s, jeniskelamin = %s, nohp = %s, tgllahir = %s, alamat = %s WHERE id = %s", [nama, jenis_kelamin, no_hp, tanggal_lahir, alamat, user_session["id"]])
            c.execute("UPDATE sijarta.pekerja SET namabank = %s, nomorrekening = %s, npwp = %s, linkfoto = %s WHERE id = %s", [nama_bank, no_rek, npwp, url_foto, user_session["id"]])
        except:
            error_message = "Nomor HP telah terdaftar."
            return render(
                request, "updateProfile.html", {"error_message": error_message, "role": role}
            )        
            
        return redirect("profile")


def worker_profile(request, id):
    c = connection.cursor()
    c.execute("SELECT * FROM sijarta.users WHERE id = %s", [id])
    user = c.fetchone()
    
    if user is None:
        raise Http404("Worker not found")
    
    c.execute("SELECT * FROM sijarta.pekerja WHERE id = %s", [id])
    user_pekerja = c.fetchone()
    context = {
        "nama" : user[1],
        "no_hp" : user[3],
        "tanggal_lahir" : user[5],
        "alamat" : user[6],    
        "url_foto": user_pekerja[4],
        "rating": user_pekerja[5],
        "jml_pesanan_selesai": user_pekerja[6]   
    }
    
    return render(request, "workerProfile.html", context)
    