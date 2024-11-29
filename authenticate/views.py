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

DUMMY_PENGGUNA = []
DUMMY_PEKERJA = []

# Halaman Registrasi untuk Pekerja
def register_pekerja(request):
    if request.method == "POST":
        nama = request.POST.get("nama")
        password = request.POST.get("password")
        jenis_kelamin = request.POST.get("jenis_kelamin")
        no_hp = request.POST.get("no_hp")
        tanggal_lahir = request.POST.get("tanggal_lahir")
        alamat = request.POST.get("alamat")
        nama_bank = request.POST.get("nama_bank")
        npwp = request.POST.get("npwp")
        url_foto = request.POST.get("url_foto")

        # Validasi No HP dan NPWP unik
        if any(u["no_hp"] == no_hp for u in DUMMY_PENGGUNA + DUMMY_PEKERJA):
            error_message = "Nomor HP telah terdaftar."
            return render(
                request,
                "authenticate/register_pekerja.html",
                {"error_message": error_message},
            )
        if any(u["npwp"] == npwp for u in DUMMY_PEKERJA):
            error_message = "Nomor NPWP telah terdaftar."
            return render(
                request,
                "authenticate/register_pekerja.html",
                {"error_message": error_message},
            )

        # Tambahkan ke DUMMY_PEKERJA
        DUMMY_PEKERJA.append(
            {
                "nama": nama,
                "password": password,
                "jenis_kelamin": jenis_kelamin,
                "no_hp": no_hp,
                "tanggal_lahir": tanggal_lahir,
                "alamat": alamat,
                "nama_bank": nama_bank,
                "npwp": npwp,
                "url_foto": url_foto,
            }
        )
        messages.success(request, "Registrasi berhasil. Silakan login.")
        return redirect("login")

    return render(request, "authenticate/register_pekerja.html")


def register(request):
    return render(request, "authenticate/register.html")


def profile(request):
    # Mendapatkan nomor HP dari session
    user = request.session.get("user", None)

    if not user:
        raise Http404("User not logged in")  # Pengguna harus login terlebih dahulu

    role = user.get("role")

    if role == "pelanggan":
        pass

    if role == "pekerja":
        pass

    context = {
        "profile": user,
    }

    return render(request, "profile.html", context)


@csrf_exempt
def updateProfile(request):
    user = request.session.get("user", None)
    if not user:
        raise Http404("User not logged in")  # Pengguna harus login terlebih dahulu

    if request.method == "POST":
        if user["role"] == "pengguna":
            user["nama"] = request.POST.get("nama")
            user["jenis_kelamin"] = request.POST.get("jenis_kelamin")
            user["no_hp"] = request.POST.get("no_hp")
            user["tanggal_lahir"] = request.POST.get("tanggal_lahir")
            user["alamat"] = request.POST.get("alamat")
        else:
            user["nama"] = request.POST.get("nama")
            user["jenis_kelamin"] = request.POST.get("jenis_kelamin")
            user["no_hp"] = request.POST.get("no_hp")
            user["tanggal_lahir"] = request.POST.get("tanggal_lahir")
            user["alamat"] = request.POST.get("alamat")
            user["nama_bank"] = request.POST.get("nama_bank")
            user["npwp"] = request.POST.get("npwp")
            user["no_rekening"] = request.POST.get("no_rekening")
            user["url_foto"] = request.POST.get("url_foto")
        return redirect("profile")

    context = {
        "profile": user,
    }

    return render(request, "updateProfile.html", context)


