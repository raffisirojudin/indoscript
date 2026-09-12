# IndoScript 🇮🇩

**IndoScript** adalah interpreter berbasis Python dengan kata kunci (*keywords*) Bahasa Indonesia. Proyek ini dilengkapi dengan antarmuka CLI `indo` agar skrip `.indo` bisa dieksekusi langsung melalui terminal.

---

## 🔄 Perubahan Sintaks (Python vs IndoScript)

| Python Standar | IndoScript | Keterangan |
| :--- | :--- | :--- |
| `print()` | `tulis()` | Menampilkan output ke layar |
| `input()` | `baca()` | Menerima input dari pengguna |
| `if` / `elif` / `else` | `jika` / `jika_tidak` / `lainnya` | Pengondisian logika |
| `for` / `while` | `selama` / `untuk` | Perulangan (*looping*) |
| `def` / `return` | `fungsi` / `kembalikan` | Fungsi dan *return value* |
| `True` / `False` | `Benar` / `Salah` | Nilai Boolean |

---

## 🚀 Cara Instalasi

Pastikan **Python 3.8+** dan **Git** sudah terpasang di sistemmu.
```
### 🪟 Windows (PowerShell / CMD)
powershell
pip install git+[https://github.com/raffisirojudin/indoscript.git](https://github.com/raffisirojudin/indoscript.git)
🍎 macOS
pip3 install git+[https://github.com/raffisirojudin/indoscript.git](https://github.com/raffisirojudin/indoscript.git)
### 🐧 Linux / WSL (Ubuntu, Debian, Arch)
bash
pip install git+[https://github.com/raffisirojudin/indoscript.git](https://github.com/raffisirojudin/indoscript.git) --break-system-packages
📦 Isolasi via pipx (Opsional)
pipx install git+[https://github.com/raffisirojudin/indoscript.git](https://github.com/raffisirojudin/indoscript.git)
