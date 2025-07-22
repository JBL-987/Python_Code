class Mobil:
    def __init__(self, merek, warna):
        self.merek = merek
        self.warna = warna
    def info(self):
        print(f"Mobil {self.merek} berwarna {self.warna}")

toyota = Mobil("toyota", "merah")
toyota.info()

class Lingkaran:
    def __init__(self, angka):
        self.angka = angka
    def luas(self):
        return self.angka**2 * 3.14

l = Lingkaran(7)
print(l.luas())


class Animal:
    def suara(self):
        print("......")

class Dog(Animal):
    def suara(self):
        print("guguk")

d = Dog()
d.suara()

class Rekening:
    def __init__(self, pengguna ,saldo):
        self._pengguna = pengguna
        self.saldo = saldo
    def lihat_saldo(self):
        return self.saldo
    def setor_saldo(self, uang):
        return uang + self.saldo

r = Rekening("jason", 5000)
print(r.lihat_saldo())
print(r.setor_saldo(2000))

class SistemAuth:
    def __init__(self):
        self.__pengguna = {
            "jason": 3000,
            "brandon": 2000,
            "loi": 6000
        }
    def login(self):
        username = input("masukkan username: ")
        password = input("masukkan password: ")
        if username in self.__pengguna and self.__pengguna[username] == password:
            return "login berhasil"
        else:
            return "login tidak berhasil"
    def tambah_akun(self):
        username = input("masukkan username: ")
        password = input("masukkan password: ")
        if username not in self.__pengguna:
            self.__pengguna[username] = password
            return "user berhasil ditambahkan"
        else:
            return "username sudah ada di daftar"
        
p = SistemAuth()
print(p.login())
print(p.tambah_akun())