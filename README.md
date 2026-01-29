# 🧾 Apart Fatura - Apartment Invoice Generator

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![PyQt5](https://img.shields.io/badge/PyQt5-GUI-green?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-blue?style=for-the-badge)

*Modern desktop application for generating apartment invoices with PDF export*

</div>

---

## 📖 Overview

Apart Fatura is a user-friendly desktop application designed for apartment managers and building administrators to easily create, customize, and export professional PDF invoices. Built with PyQt5, it offers a modern interface with template support and comprehensive invoice management.

## ✨ Features

- 🎨 **Modern UI**: Clean and intuitive PyQt5 interface
- 📄 **PDF Generation**: Professional invoice creation with customizable templates
- 🖼️ **Template Support**: Pre-designed invoice templates
- 🎯 **Easy Customization**: Quick invoice editing and personalization
- 💼 **Apartment Management**: Manage multiple apartments and tenants
- 📊 **Expense Tracking**: Itemized billing and expense categories
- 💾 **Data Persistence**: Save and load invoice data
- 🖨️ **Print Support**: Direct printing or PDF export
- 🎨 **Logo/Icon Support**: Add custom branding to invoices

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/ernakkc/Apart-Fatura.git
   cd Apart-Fatura
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   python main.py
   ```

## 📦 Dependencies

The application requires the following Python packages:

```txt
PyQt5>=5.15.0
reportlab>=3.6.0
PyPDF2>=2.0.0
```

Install all at once:
```bash
pip install PyQt5 reportlab PyPDF2
```

## 💻 Usage

### Creating an Invoice

1. **Launch the Application**:
   ```bash
   python main.py
   ```

2. **Fill in Details**:
   - Apartment number/name
   - Tenant information
   - Billing period
   - Expense items and amounts

3. **Customize Template**:
   - Select invoice template
   - Add logo or header image
   - Choose color scheme

4. **Generate PDF**:
   - Preview invoice
   - Export to PDF
   - Print or save

### Invoice Components

- **Header**: Building name, address, logo
- **Tenant Info**: Name, apartment number, contact
- **Billing Period**: Month/year
- **Expense Items**:
  - Water
  - Electricity
  - Natural Gas
  - Building Maintenance
  - Cleaning
  - Security
  - Other expenses
- **Totals**: Subtotal, tax, total amount
- **Footer**: Payment instructions, due date

## 🎨 Features in Detail

### PDF Generation

```python
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

# Generate professional invoices
invoice = InvoiceGenerator()
invoice.set_header("Building Name")
invoice.add_items(expense_list)
invoice.save("invoice.pdf")
```

### Template System

- **Default Template**: Standard invoice layout
- **Formal Template**: Professional business style
- **Modern Template**: Contemporary design
- **Custom Templates**: Create your own

### Data Management

```python
# Save invoice data
invoice_data = {
    "tenant": "John Doe",
    "apartment": "A-101",
    "items": expense_items,
    "total": 1500.00
}
save_invoice(invoice_data)

# Load previous invoices
previous = load_invoices()
```

## 📁 Project Structure

```
Apart-Fatura/
├── main.py                 # Application entry point
├── requirements.txt        # Python dependencies
├── fatura oluştur.spec    # PyInstaller spec file
├── dist/                  # Built executables
├── utils/                 # Utility modules
│   ├── invoice.py        # Invoice generation logic
│   ├── pdf_handler.py    # PDF operations
│   └── templates.py      # Template management
├── assets/               # Images, icons, logos
├── templates/            # Invoice templates
├── data/                # Saved invoice data
└── README.md            # This file
```

## 🔧 Configuration

### Custom Logo

Place your logo in `assets/logo.png` or configure path:
```python
LOGO_PATH = "path/to/your/logo.png"
```

### Default Values

Edit `config.py`:
```python
# Building Information
BUILDING_NAME = "Your Building Name"
BUILDING_ADDRESS = "Building Address"
TAX_RATE = 0.18  # 18% VAT

# Invoice Settings
CURRENCY = "TL"
DATE_FORMAT = "%d.%m.%Y"
```

### Expense Categories

Customize in `utils/categories.py`:
```python
CATEGORIES = [
    "Water (Su)",
    "Electricity (Elektrik)",
    "Natural Gas (Doğalgaz)",
    "Maintenance (Aidat)",
    "Cleaning (Temizlik)",
    "Security (Güvenlik)",
    "Elevator (Asansör)",
    "Other (Diğer)"
]
```

## 🖨️ Export Options

### PDF Export
```python
# Standard PDF
invoice.export_pdf("invoice.pdf")

# With password protection
invoice.export_pdf("invoice.pdf", password="1234")

# Multiple invoices
batch_export(invoice_list, output_dir="invoices/")
```

### Print
```python
# Direct print
invoice.print()

# Print preview
invoice.show_print_preview()
```

## 🎨 Customization

### Colors
```python
PRIMARY_COLOR = "#2196F3"
SECONDARY_COLOR = "#FFC107"
TEXT_COLOR = "#333333"
```

### Fonts
```python
HEADER_FONT = ("Arial", 16, "bold")
BODY_FONT = ("Arial", 11)
FOOTER_FONT = ("Arial", 9)
```

## 🐛 Troubleshooting

### PyQt5 Installation Issues
```bash
# Linux
sudo apt-get install python3-pyqt5

# macOS
brew install pyqt5

# Windows
pip install PyQt5 --user
```

### PDF Generation Errors
```bash
# Reinstall reportlab
pip uninstall reportlab
pip install reportlab --upgrade
```

### Font Issues
```bash
# Install required fonts
# Windows: Place TTF files in C:\Windows\Fonts
# Linux: Place in ~/.fonts/
# macOS: Place in ~/Library/Fonts/
```

## 📊 Features Roadmap

- [ ] Multi-language support (English, German)
- [ ] Email invoice directly to tenants
- [ ] Recurring invoice automation
- [ ] Payment tracking
- [ ] Expense analytics and reports
- [ ] Cloud backup
- [ ] Mobile app companion
- [ ] Online payment integration

## 🤝 Contributing

Contributions are welcome! Ideas for improvements:
- New invoice templates
- Additional expense categories
- Localization support
- Bug fixes and optimizations

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👤 Author

**Eren Akkoç**
- GitHub: [@ernakkc](https://github.com/ernakkc)
- Email: ern.akkc@gmail.com

## 🙏 Acknowledgments

- PyQt5 for the GUI framework
- ReportLab for PDF generation
- Turkish apartment management community

---

<div align="center">

**Built with ❤️ for Apartment Managers**

*Simplifying invoice management!*

⭐ Star this repo if you find it useful!

</div>
