from fpdf import FPDF
import os
import random
from template_style import get_theme, get_all_theme_names

def bersihkan_karakter(text):
    """Ganti karakter yang tidak didukung latin-1"""
    if not isinstance(text, str):
        return str(text)
    return text \
        .replace("•", "-") \
        .replace("–", "-") \
        .replace("—", "-") \
        .replace("“", '"') \
        .replace("”", '"') \
        .replace("‘", "'") \
        .replace("’", "'") \
        .replace("→", "->") \
        .replace("…", "...")

class ResumePDF(FPDF):
    def __init__(self, theme):
        super().__init__()
        self.theme = theme

    def header(self):
        self.set_fill_color(*self.theme["primary_color"])
        self.rect(0, 0, 210, 40, style='F')

    def garis_pemisah(self):
        self.set_draw_color(*self.theme["line_color"])
        self.set_line_width(0.4)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(5)

def buat_resume(data, filename, theme_name=None):
    # Pilih tema secara acak jika tidak ditentukan
    if not theme_name:
        theme_name = random.choice(get_all_theme_names())
    theme = get_theme(theme_name)

    pdf = ResumePDF(theme)
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    # Header: Nama dan Kontak
    pdf.set_xy(10, 10)
    pdf.set_font("Arial", 'B', 16)
    pdf.set_text_color(*theme["header_text_color"])
    pdf.cell(0, 10, txt=bersihkan_karakter(data.get("nama", "NAMA LENGKAP")).upper(), ln=True)

    pdf.set_font("Arial", '', 11)
    pdf.cell(0, 7, txt=bersihkan_karakter(data.get("email", "")), ln=True)
    pdf.cell(0, 7, txt=bersihkan_karakter(data.get("telepon", "")), ln=True)
    pdf.multi_cell(0, 7, txt=bersihkan_karakter(data.get("alamat", "")))
    pdf.ln(5)

    # Tambahkan foto jika tersedia
    if data.get("foto_path") and os.path.exists(data["foto_path"]):
        try:
            pdf.image(data["foto_path"], x=160, y=10, w=30, h=30)
        except Exception as e:
            print(f"[⚠️] Gagal menampilkan foto: {e}")

    pdf.set_text_color(*theme["text_color"])

    # Ringkasan Profil
    if 'ringkasan' in data:
        pdf.set_font("Arial", 'B', 13)
        pdf.set_text_color(*theme["primary_color"])
        pdf.cell(0, 10, txt="Ringkasan Profil", ln=True)
        pdf.set_font("Arial", '', 11)
        pdf.set_text_color(*theme["text_color"])
        pdf.multi_cell(0, 8, txt=bersihkan_karakter(data['ringkasan']))
        pdf.garis_pemisah()

    # Pendidikan
    if 'pendidikan' in data:
        pdf.set_font("Arial", 'B', 13)
        pdf.set_text_color(*theme["primary_color"])
        pdf.cell(0, 10, txt="Pendidikan", ln=True)
        pdf.set_font("Arial", '', 11)
        pdf.set_text_color(*theme["text_color"])
        for p in data['pendidikan']:
            pdf.multi_cell(0, 8, txt="- " + bersihkan_karakter(p))
        pdf.garis_pemisah()

    # Pengalaman Kerja
    if 'pengalaman' in data:
        pdf.set_font("Arial", 'B', 13)
        pdf.set_text_color(*theme["primary_color"])
        pdf.cell(0, 10, txt="Pengalaman Kerja", ln=True)
        pdf.set_font("Arial", '', 11)
        pdf.set_text_color(*theme["text_color"])
        for exp in data['pengalaman']:
            pdf.multi_cell(0, 8, txt="- " + bersihkan_karakter(exp))
        pdf.garis_pemisah()

    # Keahlian
    if 'skill' in data:
        pdf.set_font("Arial", 'B', 13)
        pdf.set_text_color(*theme["primary_color"])
        pdf.cell(0, 10, txt="Keahlian", ln=True)
        pdf.set_font("Arial", '', 11)
        pdf.set_text_color(*theme["text_color"])
        pdf.multi_cell(0, 8, txt="- " + " | ".join([bersihkan_karakter(s) for s in data['skill']]))
        pdf.garis_pemisah()

    # Simpan PDF
    pdf.output(filename)
