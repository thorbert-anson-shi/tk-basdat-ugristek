from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import Http404

# Variabel global untuk menyimpan data dummy
# Dummy data untuk Pengguna
DUMMY_PENGGUNA = [
    {
        "nama": "Pengguna 1",
        "password": "password123",
        "jenis_kelamin": "L",
        "no_hp": "08123456789",
        "tanggal_lahir": "1995-06-15",
        "alamat": "Jl. Contoh No. 1",
        "role": "pengguna",
        "saldo_mypay": 1000000

    },
    {
        "nama": "Pengguna 2",
        "password": "password456",
        "jenis_kelamin": "P",
        "no_hp": "08198765432",
        "tanggal_lahir": "1990-03-22",
        "alamat": "Jl. Contoh No. 2",
        "role": "pengguna",
        "saldo_mypay": 1000000
    }
]

# Dummy data untuk Pekerja
DUMMY_PEKERJA = [
    {
        "nama": "Pekerja 1",
        "password": "password789",
        "jenis_kelamin": "L",
        "no_hp": "08987654321",
        "tanggal_lahir": "1985-10-30",
        "alamat": "Jl. Pekerja No. 1",
        "npwp": "123456789012345",
        "nama_bank": "GoPay",
        "no_rekening": "9876543210",
        "url_foto": "https://example.com/images/worker1.jpg",  # URL foto pekerja
        "role": "pekerja",
        "rating": 4.5,
        "saldo_mypay": 1000000
    },
    {
        "nama": "Pekerja 2",
        "password": "password101112",
        "jenis_kelamin": "P",
        "no_hp": "08965432109",
        "tanggal_lahir": "1988-11-15",
        "alamat": "Jl. Pekerja No. 2",
        "npwp": "987654321098765",
        "nama_bank": "OVO",
        "no_rekening": "1234567890",
        "url_foto": "https://example.com/images/worker2.jpg",  # URL foto pekerja
        "role": "pekerja",
        "rating": 4.5,
        "saldo_mypay": 1000000
        
    }
]

# Halaman Awal
def begin(request):
    return render(request, "authenticate/index.html")  

def login(request):
    if request.method == 'POST':
        phone = request.POST.get('no_hp')
        password = request.POST.get('password')

        if not phone or not password:
            error_message = "No HP atau password tidak boleh kosong."
            return render(request, 'authenticate/login.html', {'error_message': error_message})

        # Cek data pengguna
        user = None
        for pengguna in DUMMY_PENGGUNA:
            if pengguna['no_hp'] == phone and pengguna['password'] == password:
                user = pengguna
                break

        # Cek data pekerja jika tidak ditemukan di pengguna
        if not user:
            for pekerja in DUMMY_PEKERJA:
                if pekerja['no_hp'] == phone and pekerja['password'] == password:
                    user = pekerja
                    break

        if user:
            # Simpan informasi user di session atau cookie
            request.session['user'] = user  # Simpan data pengguna di session
            return redirect('navbar')  # Redirect ke halaman utama setelah login
        else:
            error_message = "No HP atau password salah"
            return render(request, 'authenticate/login.html', {'error_message': error_message})

    return render(request, 'authenticate/login.html')


# Halaman Logout
def logout(request):
    if "user" in request.session:
        del request.session["user"]  # Hapus sesi pengguna
    return redirect("login")

# Halaman Registrasi untuk Pengguna
def register_pengguna(request):
    if request.method == "POST":
        nama = request.POST.get("nama")
        password = request.POST.get("password")
        jenis_kelamin = request.POST.get("jenis_kelamin")
        no_hp = request.POST.get("no_hp")
        tanggal_lahir = request.POST.get("tanggal_lahir")
        alamat = request.POST.get("alamat")

        # Validasi No HP unik
        if any(u["no_hp"] == no_hp for u in DUMMY_PENGGUNA + DUMMY_PEKERJA):
            error_message = "Nomor HP telah terdaftar."
            return render(request, 'authenticate/register_pengguna.html', {'error_message': error_message})

        # Tambahkan ke DUMMY_PENGGUNA
        DUMMY_PENGGUNA.append(
            {
                "nama": nama,
                "password": password,
                "jenis_kelamin": jenis_kelamin,
                "no_hp": no_hp,
                "tanggal_lahir": tanggal_lahir,
                "alamat": alamat,
            }
        )
        messages.success(request, "Registrasi berhasil. Silakan login.")
        return redirect("login")

    return render(request, "authenticate/register_pengguna.html")

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
            return render(request, 'authenticate/register_pekerja.html', {'error_message': error_message})
        if any(u["npwp"] == npwp for u in DUMMY_PEKERJA):
            error_message = "Nomor NPWP telah terdaftar."
            return render(request, 'authenticate/register_pekerja.html', {'error_message': error_message})

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

def navbar(request):
    return render(request, "navbar.html")

def profile(request):
    # Mendapatkan nomor HP dari session
    user = request.session.get('user', None)

    if not user:
        raise Http404("User not logged in")  # Pengguna harus login terlebih dahulu

    role = user.get('role', 'pengguna')  # Mengambil role dari data pengguna yang ada di session

    context = {
        'profile': user,
    }

    return render(request, 'profile.html', context)