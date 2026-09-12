import sys
import re

class ReturnException(Exception):
    def __init__(self, value):
        self.value = value

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
                print(f"Error di baris {baris_ke}: Perintah '{baris}' tidak dikenal.")

        except ReturnException:
            raise
        except Exception as e:
            print(f"Error di baris {baris_ke}: {e}")

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

def main():
    if len(sys.argv) < 2:
        print("Penggunaan: indo <nama_file.indo>")
    else:
        nama_file = sys.argv[1]
        try:
            with open(nama_file, "r") as f:
                baris_mentah = f.readlines()
            
            daftar_baris = [(idx + 1, baris) for idx, baris in enumerate(baris_mentah)]
            interpreter = Interpreter()
            interpreter.jalankan_blok(daftar_baris)
        except FileNotFoundError:
            print(f"Error: File '{nama_file}' tidak ditemukan.")

if __name__ == "__main__":
    main()