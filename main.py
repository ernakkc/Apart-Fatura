import sys
import os
import io
import webbrowser
from datetime import datetime, timedelta
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout,
    QFormLayout, QDateEdit, QDoubleSpinBox, QMessageBox, QComboBox, QTimeEdit, QTextEdit
)
from PyQt5.QtCore import QDate, QTime
from PyQt5.QtGui import QFont, QIcon
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from PyPDF2 import PdfReader, PdfWriter

class InvoiceApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Fatura Oluştur")
        icon_path = os.path.join(os.path.dirname(__file__), "utils" ,"icon.ico")
        self.setWindowIcon(QIcon(icon_path))
        
        self.setGeometry(100, 100, 500, 450)
        self.setStyleSheet("""
            QWidget {
                background: #f7f7fa;
            }
            QLabel {
                font-size: 15px;
                color: #333;
            }
            QLineEdit, QDateEdit, QDoubleSpinBox, QComboBox, QTimeEdit {
                padding: 6px;
                border: 1px solid #bbb;
                border-radius: 6px;
                font-size: 14px;
            }
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #6a82fb, stop:1 #fc5c7d);
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px 20px;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #fc5c7d, stop:1 #6a82fb);
            }
        """)
        self.init_ui()

    def init_ui(self):
        layout = QFormLayout()

        self.name_edit = QLineEdit()
        layout.addRow("Misafir Adı:", self.name_edit)

        self.checkin_edit = QDateEdit()
        self.checkin_edit.setCalendarPopup(True)
        self.checkin_edit.setDate(QDate.currentDate())
        layout.addRow("Check-in Tarihi:", self.checkin_edit)

        self.checkout_edit = QDateEdit()
        self.checkout_edit.setCalendarPopup(True)
        self.checkout_edit.setDate(QDate.currentDate().addDays(1))
        layout.addRow("Check-out Tarihi:", self.checkout_edit)

        self.rate_edit = QDoubleSpinBox()
        self.rate_edit.setRange(0, 10000)
        self.rate_edit.setValue(100.0)
        self.rate_edit.setSuffix(" $")
        layout.addRow("Günlük Fiyat:", self.rate_edit)

        # Kat ve oda numarası
        self.kat_edit = QComboBox()
        self.kat_edit.addItems(list(self.KAT_ODALAR.keys()))
        self.kat_edit.currentTextChanged.connect(self.update_oda_combo)
        layout.addRow("Kat:", self.kat_edit)

        self.oda_edit = QComboBox()
        self.oda_edit.currentTextChanged.connect(self.update_oda_tipi)
        layout.addRow("Oda Numarası:", self.oda_edit)

        self.oda_tipi_edit = QLineEdit()
        self.oda_tipi_edit.setReadOnly(True)
        layout.addRow("Oda Tipi:", self.oda_tipi_edit)

        self.update_oda_combo(self.kat_edit.currentText())

        self.arrival_date_edit = QDateEdit()
        self.arrival_date_edit.setCalendarPopup(True)
        self.arrival_date_edit.setDate(QDate.currentDate())
        layout.addRow("Geliş Tarihi:", self.arrival_date_edit)

        self.arrival_time_edit = QTimeEdit()
        self.arrival_time_edit.setTime(QTime(12, 0))
        layout.addRow("Geliş Saati:", self.arrival_time_edit)

        self.generate_btn = QPushButton("Fatura Oluştur")
        self.generate_btn.clicked.connect(self.generate_invoice)
        layout.addRow(self.generate_btn)

        self.clear_btn = QPushButton("Temizle")
        self.clear_btn.clicked.connect(self.clear_fields)
        layout.addRow(self.clear_btn)

        self.exit_btn = QPushButton("Çıkış")
        self.exit_btn.clicked.connect(self.close_app)
        layout.addRow(self.exit_btn)

        """Developed by Eren AKKOÇ"""
        self.QLabel = QLabel("©️ Developed by Eren AKKOÇ")
        self.QLabel.setStyleSheet("color: #333; font-size: 10px; font-weight: bold; text-align: center;")
        layout.addRow(self.QLabel)


        self.setLayout(layout)

    def close_app(self):
        sys.exit(0)

    def clear_fields(self):
        self.name_edit.clear()
        self.checkin_edit.setDate(QDate.currentDate())
        self.checkout_edit.setDate(QDate.currentDate().addDays(1))
        self.rate_edit.setValue(100.0)
        self.kat_edit.setCurrentText("-")
        self.oda_edit.setCurrentText("-")

    def draw_text(self, canvas_obj, x, y, text, font_size=12, is_Bold=False):
        canvas_obj.setFont("Helvetica-Bold" if is_Bold else "Helvetica", font_size)
        canvas_obj.drawString(x, y, text)
        canvas_obj.setFont("Helvetica", 12)

    KAT_ODALAR = {
        "-": [],
        "-1. Floor": [14],
        "Ground Floor": [1, 2],
        "1. Floor": [3, 4],
        "2. Floor": [5, 6],
        "3. Floor": [8, 9, 10, 11],
        "4. Floor": [12, 13],
    }
    ODA_TIPLERI = {
        "-": "-",
        1: "1+1",
        2: "1+1",
        3: "1+1",
        4: "2+1",
        5: "1+1",
        6: "2+1",
        8: "1+0",
        9: "1+0",
        10: "1+0",
        11: "1+0",
        12: "1+0",
        13: "1+0",
        14: "1+0",
    }

    def update_oda_combo(self, kat):
        self.oda_edit.blockSignals(True)
        self.oda_edit.clear()
        odalar = self.KAT_ODALAR.get(kat, [])
        for oda in odalar:
            self.oda_edit.addItem(str(oda))
        self.oda_edit.blockSignals(False)
        self.update_oda_tipi(self.oda_edit.currentText())

    def update_oda_tipi(self, oda_no):
        try:
            oda_no_int = int(oda_no)
            tipi = self.ODA_TIPLERI.get(oda_no_int, "-")
        except Exception:
            tipi = "-"
        self.oda_tipi_edit.setText(tipi)

    def invoice_create_pdf(self, name, check_in, check_out, daily_rate, kat, oda_no, oda_tipi, arrival_date, arrival_time):
        invoice_created_date = datetime.now().strftime("%d %B %Y %H:%M")
        check_in_date = datetime.strptime(check_in, "%d-%m-%Y")
        check_out_date = datetime.strptime(check_out, "%d-%m-%Y")
        days_count = (check_out_date - check_in_date).days
        total_amount = days_count * daily_rate

        packet = io.BytesIO()
        can = canvas.Canvas(packet, pagesize=A4)
        can.setTitle("Invoice")

        self.draw_text(can, 70, 680, "NAME:", is_Bold=True)
        self.draw_text(can, 115, 680, name)
        self.draw_text(can, 450, 680, "Invoice Date:", is_Bold=True)
        self.draw_text(can, 450, 665, invoice_created_date)
        self.draw_text(can, 70, 665, "Floor:", is_Bold=True)
        self.draw_text(can, 113, 665, kat)
        self.draw_text(can, 70, 650, "Room No:", is_Bold=True)
        self.draw_text(can, 130, 650, oda_no)
        self.draw_text(can, 70, 635, "Room Type:", is_Bold=True)
        self.draw_text(can, 142, 635, oda_tipi)
        self.draw_text(can, 70, 620, "Flight Arrival:", is_Bold=True)
        self.draw_text(can, 150, 620, f"{arrival_date} {arrival_time}")
        self.draw_text(can, 80, 580, "CHECK-IN:", is_Bold=True)
        self.draw_text(can, 140, 580, check_in + "   02:00 PM")

        write_y = 560
        for day in range(days_count):
            day_date = check_in_date + timedelta(days=day)
            self.draw_text(can, 90, write_y - day * 20, f"Day {day + 1}:", is_Bold=True, font_size=10)
            self.draw_text(can, 130, write_y - day * 20, day_date.strftime("%d %B %Y"), font_size=10)

        y_after_days = write_y - (days_count + 1) * 20
        self.draw_text(can, 80, y_after_days + 20, "CHECK-OUT:", is_Bold=True)
        self.draw_text(can, 170, y_after_days + 20, check_out + "   11:00 AM")
        self.draw_text(can, 70, y_after_days - 10, f"Daily Rate: {daily_rate} $", is_Bold=True)
        self.draw_text(can, 70, y_after_days - 30, f"Total Amount: {daily_rate} x {days_count} = {total_amount} $", is_Bold=True)

        text = """
        CHECK-IN time is no earlier than 02:00 PM, and CHECK-OUT time is no later than 11:00 AM.
        Wi-Fi Password: 12345678961
        Dear guest, thank you for choosing us.
        It was our great pleasure to provide you with a pleasant and comfortable stay.
        We look forward to welcoming you again.
        Wishing you health and happiness.
        Balekoglu Apart Family
        """

        lines = text.strip().split('\n')
        base_y = y_after_days - 60
        for i, line in enumerate(lines):
            self.draw_text(can, 70, base_y - (i * 12), line.strip(), font_size=8)

        can.save()
        packet.seek(0)

        text_pdf = PdfReader(packet)
        pdf_path = os.path.join(os.path.dirname(__file__), "utils" ,"def.pdf")
        template_pdf = PdfReader(pdf_path)
        output = PdfWriter()
        page = template_pdf.pages[0]
        page.merge_page(text_pdf.pages[0])
        output.add_page(page)

        if not os.path.exists("faturalar"):
            os.makedirs("faturalar")
        out_path = f"faturalar/{name}.pdf"
        with open(out_path, "wb") as f:
            output.write(f)

        return out_path

    def generate_invoice(self):
        name = self.name_edit.text().strip()
        check_in = self.checkin_edit.date().toString("dd-MM-yyyy")
        check_out = self.checkout_edit.date().toString("dd-MM-yyyy")
        daily_rate = self.rate_edit.value()
        kat = self.kat_edit.currentText()
        oda_no = self.oda_edit.currentText()
        oda_tipi = self.oda_tipi_edit.text()
        arrival_date = self.arrival_date_edit.date().toString("dd-MM-yyyy")
        arrival_time = self.arrival_time_edit.time().toString("HH:mm")

        if not name or not oda_no or self.checkin_edit.date() >= self.checkout_edit.date():
            QMessageBox.critical(self, "Error", "Please fill all fields correctly.")
            return

        try:
            path = self.invoice_create_pdf(name, check_in, check_out, daily_rate, kat, oda_no, oda_tipi, arrival_date, arrival_time)
            QMessageBox.information(self, "Success", f"Invoice created: {path}")
            path = os.path.join(os.getcwd(), path)
            webbrowser.open(path)
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = InvoiceApp()
    window.show()
    sys.exit(app.exec_()) 
    
    
    
    