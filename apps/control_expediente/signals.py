import os
import subprocess
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.files import File
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

from .models import Seguimiento, Gasto


def convertir_word_a_pdf(word_path, pdf_path):
    try:
        subprocess.run([
            "libreoffice", "--headless", "--convert-to", "pdf", "--outdir",
            os.path.dirname(pdf_path), word_path
        ], check=True)
        return True
    except Exception as e:
        print("⚠ Error LibreOffice:", e)
        return False


def convertir_imagen_a_pdf(image_path, pdf_path):
    try:
        image = Image.open(image_path)
        if image.mode in ("RGBA", "P"):
            image = image.convert("RGB")

        image.save(pdf_path, "PDF", resolution=100.0)
        return True
    except Exception as e:
        print("⚠ Error al convertir imagen a PDF:", e)
        return False


def procesar_archivo(instance):
    if not instance.pdf:
        return

    file_path = instance.pdf.path
    ext = os.path.splitext(file_path)[1].lower()
    pdf_name = os.path.splitext(instance.pdf.name)[0] + ".pdf"
    pdf_path = os.path.join(os.path.dirname(file_path), os.path.basename(pdf_name))

    convertido = False
    if ext in [".doc", ".docx"]:
        convertido = convertir_word_a_pdf(file_path, pdf_path)
    elif ext in [".jpg", ".jpeg", ".png"]:
        convertido = convertir_imagen_a_pdf(file_path, pdf_path)

    if not convertido or not os.path.exists(pdf_path):
        return

    with open(pdf_path, "rb") as f:
        instance.pdf.save(os.path.basename(pdf_name), File(f), save=False)

    try:
        os.remove(file_path)
        os.remove(pdf_path)
    except:
        pass

    instance.save(update_fields=["pdf"])


@receiver(post_save, sender=Seguimiento)
def convertir_pdf_seguimiento(sender, instance, **kwargs):
    procesar_archivo(instance)


@receiver(post_save, sender=Gasto)
def convertir_pdf_gasto(sender, instance, **kwargs):
    procesar_archivo(instance)
