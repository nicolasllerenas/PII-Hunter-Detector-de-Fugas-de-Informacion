import os
import re
import pandas as pd
import PyPDF2
from colorama import Fore, Style, init
from datetime import datetime

# Inicializar colores
init(autoreset=True)

# --- 1. PATRONES DE BÚSQUEDA (El Cerebro) ---
# Aquí definimos qué es "información sensible"
PATTERNS = {
    "DNI_PERU": r"\b\d{8}\b",  # 8 dígitos exactos
    "EMAIL_CORP": r"[a-zA-Z0-9._%+-]+@empresa\.com", # Emails de la empresa
    "VISA_CARD": r"\b4[0-9]{12}(?:[0-9]{3})?\b", # Patrón básico de Visa
    "AWS_KEY": r"AKIA[0-9A-Z]{16}", # Patrón de llaves de Amazon AWS
    "PRIVATE_KEY": r"-----BEGIN PRIVATE KEY-----"
}

def extract_text_from_file(filepath):
    """Lee el contenido de archivos TXT o PDF."""
    text = ""
    try:
        if filepath.endswith('.txt') or filepath.endswith('.csv') or filepath.endswith('.md'):
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                text = f.read()
        elif filepath.endswith('.pdf'):
            with open(filepath, 'rb') as f:
                reader = PyPDF2.PdfReader(f)
                for page in reader.pages:
                    text += page.extract_text() + "\n"
    except Exception as e:
        print(f"{Fore.RED}[Error] No se pudo leer {filepath}: {e}")
    return text

def scan_directory(directory):
    """Recorre las carpetas buscando amenazas."""
    findings = []
    
    print(f"{Fore.CYAN}--- Iniciando Escaneo en: {directory} ---")
    
    for root, dirs, files in os.walk(directory):
        for file in files:
            filepath = os.path.join(root, file)
            content = extract_text_from_file(filepath)
            
            # Revisar cada patrón contra el contenido del archivo
            for p_name, p_regex in PATTERNS.items():
                matches = re.findall(p_regex, content)
                if matches:
                    print(f"{Fore.YELLOW}[ALERTA] {p_name} detectado en: {file}")
                    for match in matches:
                        # Ofuscamos el dato para el reporte (Seguridad ante todo)
                        safe_match = match[:4] + "****" 
                        findings.append({
                            "File": file,
                            "Path": filepath,
                            "Type": p_name,
                            "Snippet": safe_match,
                            "Date": datetime.now().strftime("%Y-%m-%d %H:%M")
                        })
    return findings

if __name__ == "__main__":
    # Carpeta a escanear (pon '.' para escanear la carpeta actual)
    target_folder = "./documentos_prueba" 
    
    # Crear carpeta fake si no existe para probar
    if not os.path.exists(target_folder):
        os.makedirs(target_folder)
        with open(f"{target_folder}/empleados.txt", "w") as f:
            f.write("Juan Perez DNI: 12345678, Email: juan@empresa.com")
        print(f"{Fore.GREEN}Carpeta de prueba creada. ¡Pon archivos ahí!")

    results = scan_directory(target_folder)
    
    if results:
        df = pd.DataFrame(results)
        report_name = f"security_report_{datetime.now().strftime('%Y%m%d')}.csv"
        df.to_csv(report_name, index=False)
        print(f"\n{Fore.GREEN}✅ Reporte de Incidentes generado: {report_name}")
    else:
        print(f"\n{Fore.GREEN}✅ No se encontraron fugas de información.")