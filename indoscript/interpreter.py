import sys
import re

class ReturnException(Exception):
    def __init__(self, value):
        self.value = value

# Map tipe eksepsi Python bawaan ke Bahasa Indonesia
KAMUS_EROR = {
    "ZeroDivisionError": "KesalahanBagiNol",
    "NameError": "KesalahanNama",
    "TypeError": "KesalahanTipe",
    "ValueError": "KesalahanNilai",
}

class Interpreter:
    def __init__(self):
        self.memori = {}
        self.fungsi_map = {}

    def panggil_fungsi(self, nama_fn, *args):
        if nama_fn not in self.fungsi_map:
            raise Exception(f"Fungsi '{nama_fn}' belum dibuat.")
        
        params, blok_fn = self.fungsi_map[nama_fn]
        if len(params) != len(args):
            raise Exception(f"Fungsi '{nama_fn}' butuh {len(params)} argumen, tapi diberi {len(args)}.")
        
        memori_lokal = self.memori.copy()
        for p, a in zip(params, args):
            memori_lokal[p] = a
        
        try:
            self.jalankan_blok(blok_fn, memori_lokal)
        except ReturnException as ret:
            return ret.value
        return None

    def evaluasi_ekspresi(self, ekspresi, memori_lokal):
        def replacer(match):
            fn_name = match.group(1)
            args_str = match.group(2)
            return f"__panggil('{fn_name}'{', ' + args_str if args_str.strip() else ''})"

        ekspresi_mod = re.sub(r'panggil\s+([a-zA-Z_]\w*)\s*\((.*?)\)', replacer, ekspresi)

        context = {
            "__panggil": lambda fn_name, *args: self.panggil_fungsi(fn_name, *args),
            "str": str, "int": int, "float": float, "len": len, "list": list
        }
        return eval(ekspresi_mod, context, memori_lokal)

    def eksekusi_baris(self, baris, baris_ke):
        try:
            if baris.startswith("kembalikan "):
                ekspresi = baris[11:].strip()
                val = self.evaluasi_ekspresi(ekspresi, self.memori)
                raise ReturnException(val)

            elif baris.startswith("panggil "):
                self.evaluasi_ekspresi(baris, self.memori)

            elif baris.startswith("tanya "):
                bagian = baris[6:].split("=")
                nama_var = bagian[0].strip()
                prompt = bagian[1].strip().strip('"')
                jawaban = input(prompt + " ")
                self.memori[nama_var] = int(jawaban) if jawaban.isdigit() else jawaban

            elif baris.startswith("simpan "):
                bagian = baris[7:].split("=", 1)
                nama_var = bagian[0].strip()
                ekspresi = bagian[1].strip()
                self.memori[nama_var] = self.evaluasi_ekspresi(ekspresi, self.memori)

            elif baris.startswith("cetak "):
                isi = baris[6:].strip()
                hasil = self.evaluasi_ekspresi(isi, self.memori)
                print(hasil)

            else:
                print(f"[KesalahanSintaks] Baris {baris_ke}: Perintah '{baris}' tidak dikenal.")

        except ReturnException:
            raise
        except Exception as e:
            nama_eror = type(e).__name__
            nama_id = KAMUS_EROR.get(nama_eror, nama_eror)
            print(f"[{nama_id}] Baris {baris_ke}: {e}")

    def jalankan_blok(self, daftar_baris, memori_custom=None):
        memori_awal = self.memori
        if memori_custom is not None:
            self.memori = memori_custom

        i = 0
        while i < len(daftar_baris):
            baris_ke, baris = daftar_baris[i]
            baris = baris.strip()

            if not baris or baris.startswith("#"):
                i += 1
                continue

            if baris.startswith("fungsi "):
                sisa = baris[7:].strip()
                nama_fn = sisa.split("(")[0].strip()
                params_raw = sisa[sisa.find("(")+1 : sisa.rfind(")")]
                params = [p.strip() for p in params_raw.split(",") if p.strip()]

                i += 1
                blok_fn = []
                while i < len(daftar_baris) and daftar_baris[i][1].strip() != "selesai":
                    blok_fn.append(daftar_baris[i])
                    i += 1
                self.fungsi_map[nama_fn] = (params, blok_fn)

            elif baris.startswith("ulang ") and baris.endswith(" kali"):
                jumlah = int(self.evaluasi_ekspresi(baris[6:-5].strip(), self.memori))
                i += 1
                blok = []
                while i < len(daftar_baris) and daftar_baris[i][1].strip() != "selesai":
                    blok.append(daftar_baris[i])
                    i += 1
                for _ in range(jumlah):
                    self.jalankan_blok(blok)

            elif baris.startswith("jika ") and baris.endswith(" maka"):
                kondisi = baris[5:-5].strip()
                i += 1
                blok_maka, blok_kalau_tidak = [], []
                di_kalau_tidak = False

                while i < len(daftar_baris) and daftar_baris[i][1].strip() != "selesai":
                    if daftar_baris[i][1].strip() == "kalau_tidak":
                        di_kalau_tidak = True
                    else:
                        (blok_kalau_tidak if di_kalau_tidak else blok_maka).append(daftar_baris[i])
                    i += 1

                if self.evaluasi_ekspresi(kondisi, self.memori):
                    self.jalankan_blok(blok_maka)
                else:
                    self.jalankan_blok(blok_kalau_tidak)

            else:
                self.eksekusi_baris(baris, baris_ke)

            i += 1

        self.memori = memori_awal


def mulai_repl():
    """Shell Interaktif untuk IndoScript"""
    print("=== IndoScript 0.1.0 Interactive Shell ===")
    print("Ketik 'keluar' atau tekan Ctrl+C untuk berhenti.\n")
    
    interpreter = Interpreter()
    baris_ke = 1

    while True:
        try:
            baris_input = input("indo> ")
            if baris_input.strip() == "keluar":
                break
            if not baris_input.strip():
                continue

            daftar_baris = [(baris_ke, baris_input)]
            baris_ke += 1

            # Deteksi pembuka blok untuk mendukung multi-line REPL
            b_strip = baris_input.strip()
            butuh_blok = (
                b_strip.startswith("fungsi ") or 
                (b_strip.startswith("jika ") and b_strip.endswith(" maka")) or 
                (b_strip.startswith("ulang ") and b_strip.endswith(" kali"))
            )

            if butuh_blok:
                kedalaman = 1
                while kedalaman > 0:
                    sub_baris = input("...   ")
                    s_strip = sub_baris.strip()
                    if s_strip.startswith("fungsi ") or (s_strip.startswith("jika ") and s_strip.endswith(" maka")) or (s_strip.startswith("ulang ") and s_strip.endswith(" kali")):
                        kedalaman += 1
                    elif s_strip == "selesai":
                        kedalaman -= 1
                    daftar_baris.append((baris_ke, sub_baris))
                    baris_ke += 1

            interpreter.jalankan_blok(daftar_baris)

        except (KeyboardInterrupt, EOFError):
            print("\nSampai jumpa!")
            break


def main():
    if len(sys.argv) < 2:
        mulai_repl()
    else:
        nama_file = sys.argv[1]
        try:
            with open(nama_file, "r") as f:
                baris_mentah = f.readlines()
            
            daftar_baris = [(idx + 1, baris) for idx, baris in enumerate(baris_mentah)]
            interpreter = Interpreter()
            interpreter.jalankan_blok(daftar_baris)
        except FileNotFoundError:
            print(f"[BerkasTidakDitemukan] File '{nama_file}' tidak ditemukan.")

if __name__ == "__main__":
    main()
