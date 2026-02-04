# 🛡️ PII-Hunter: Automated Data Loss Prevention (DLP) Scanner

![Python](https://img.shields.io/badge/Python-3.10-blue?style=for-the-badge&logo=python)
![Security](https://img.shields.io/badge/Security-DLP-red?style=for-the-badge&logo=hack-the-box)
![Compliance](https://img.shields.io/badge/Compliance-GDPR%2FLPDP-green?style=for-the-badge)

## 📌 Descripción General

**PII-Hunter** es una herramienta de **Automatización de Seguridad (DevSecOps)** diseñada para auditar directorios y repositorios en busca de información sensible expuesta.

El script simula un motor de **DLP (Data Loss Prevention)**, escaneando archivos (PDF, TXT, CSV, MD) mediante patrones de Expresiones Regulares (Regex) para identificar:
* 🆔 **Documentos de Identidad** (DNI Perú).
* 💳 **Datos Financieros** (Tarjetas de Crédito Visa/Mastercard).
* 🔑 **Credenciales Cloud** (AWS Keys, Private Keys).
* 📧 **Información Corporativa** (Emails internos).

Este proyecto demuestra cómo automatizar la detección de riesgos de privacidad y cumplimiento normativo (ISO 27001).

## 🚀 Características Clave

* **Multi-Formato:** Capacidad para leer y extraer texto de archivos planos y **PDFs** (usando `PyPDF2`).
* **Motor Regex Personalizable:** Detección de patrones complejos con validación de formatos.
* **Reportes de Auditoría:** Generación automática de reportes en **CSV** con los hallazgos (Data Cleaning con `Pandas`).
* **Alertas Visuales:** Interfaz de línea de comandos (CLI) con alertas de colores para identificación rápida de amenazas.

## 🛠️ Stack Tecnológico

* **Lenguaje:** Python 3.10+
* **Librerías Core:**
    * `pandas`: Estructuración y exportación de reportes.
    * `PyPDF2`: Extracción de texto en documentos binarios.
    * `re`: Módulo nativo para Expresiones Regulares avanzadas.
    * `colorama`: UX para la terminal.

## ⚙️ Instalación y Uso

1.  **Clonar el repositorio:**
    ```bash
    git clone [https://github.com/nicolasllerenas/PII-Hunter.git](https://github.com/nicolasllerenas/PII-Hunter.git)
    cd PII-Hunter
    ```

2.  **Crear entorno virtual e instalar dependencias:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # En Windows: venv\Scripts\activate
    pip install -r requirements.txt
    ```

3.  **Ejecutar el escáner:**
    ```bash
    python scanner.py
    ```

## 🔍 Patrones de Detección (Ejemplo)

El sistema utiliza un diccionario de reglas configurables en `scanner.py`:

```python
PATTERNS = {
    "DNI_PERU": r"\b\d{8}\b",               # 8 dígitos exactos
    "VISA_CARD": r"\b4[0-9]{12}(?:[0-9]{3})?\b", # Estándar Visa
    "AWS_KEY": r"AKIA[0-9A-Z]{16}",         # Access Keys de Amazon
    "EMAIL_CORP": r"[a-zA-Z0-9._%+-]+@empresa\.com"
}