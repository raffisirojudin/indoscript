# IndoScript

**IndoScript** adalah interpreter Python dengan kata kunci (*keywords*) berlayar Bahasa Indonesia. Proyek ini dibuat agar penulisan logika pemrograman terasa lebih natural bagi penutur Bahasa Indonesia, sekaligus dilengkapi perintah CLI `indo` untuk mengeksekusi skrip dari terminal secara global.

---

## 🔄 Apa Bedanya dengan Python Biasa?

IndoScript mengubah kata kunci standar Python menjadi kosakata Bahasa Indonesia. Berikut adalah tabel perubahan padanan sintaks dasarnya:

| Python Standar | IndoScript | Keterangan / Contoh |
| :--- | :--- | :--- |
| `print()` | `tulis()` | Menampilkan output ke layar |
| `input()` | `baca()` | Menerima masukan pengguna |
| `if` | `jika` | Pengondisian utama |
| `elif` | `jika_tidak` | Pengondisian alternatif |
| `else` | `lainnya` | Kondisi terakhir |
| `for` / `while` | `selama` / `untuk` | Perulangan |
| `def` | `fungsi` | Deklarasi fungsi baru |
| `return` | `kembalikan` | Mengembalikan nilai fungsi |
| `True` / `False` | `Benar` / `Salah` | Nilai boolean |

*(Catatan: Kamu bisa menyesuaikan tabel padanan di atas sesuai dengan kata kunci aktual yang kamu atur di `interpreter.py`).*

---

## 🚀 Cara Instalasi

Jalankan perintah ini di terminal untuk menginstal IndoScript langsung dari GitHub:

```bash
pip install git+[https://github.com/raffisirojudin/indoscript.git](https://github.com/raffisirojudin/indoscript.git)
