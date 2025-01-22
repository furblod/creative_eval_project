from difflib import SequenceMatcher
import os
import pandas as pd
from test_verilog import test_verilog_code


def calculate_fluency(verilog_code):
    required_keywords = ["module", "input", "output", "assign", "endmodule"]
    keyword_count = sum(1 for keyword in required_keywords if keyword in verilog_code)

    # Gerekli anahtar kelimeler üzerinden puanlama
    ratio = keyword_count / len(required_keywords)

    if ratio == 1.0:
        return 1.0  # Tüm yapılar eksiksiz
    elif ratio >= 0.7:
        return 0.8  # Çoğu yapı mevcut
    elif ratio >= 0.4:
        return 0.5  # Kısmen akıcı
    else:
        return 0.0  # Çok düşük akıcılık

def calculate_flexibility(verilog_code):
    assign_count = verilog_code.count("assign")
    always_count = verilog_code.count("always")
    wire_count = verilog_code.count("wire")

    # Esnekliği değerlendir: alternatif yapıların varlığı
    if assign_count > 1 and always_count > 0 and wire_count > 0:
        return 1.0  # Çok esnek
    elif assign_count > 1 and (always_count > 0 or wire_count > 0):
        return 0.8  # Orta derecede esnek
    elif assign_count > 0:
        return 0.5  # Düşük esneklik
    else:
        return 0.0  # Hiç esnek değil

def calculate_originality(verilog_code, module_type):
    reference_codes = {
        "adder": """module adder(input a, input b, input cin, output sum, output cout);
    assign sum = a ^ b ^ cin;
    assign cout = (a & b) | (b & cin) | (a & cin);
endmodule""",
        "mux": """module mux_2to1(input a, input b, input sel, output y);
    assign y = (sel) ? b : a;
endmodule"""
    }

    reference_code = reference_codes.get(module_type, "")
    similarity = SequenceMatcher(None, verilog_code.strip(), reference_code.strip()).ratio()

    if similarity < 0.7:
        return 1.0  # Çok özgün
    elif 0.7 <= similarity < 0.9:
        return 0.5  # Kısmen özgün
    else:
        return 0.0  # Tipik çözüm

def calculate_elaboration(verilog_code):
    comments = [line for line in verilog_code.splitlines() if "//" in line or "/*" in line]
    comment_ratio = len(comments) / len(verilog_code.splitlines()) if verilog_code.splitlines() else 0.0

    # Yorum oranına göre detaylandırma
    if comment_ratio > 0.3:
        return 1.0  # Çok detaylı
    elif 0.1 <= comment_ratio <= 0.3:
        return 0.5  # Orta düzey detay
    else:
        return 0.0  # Hiç detay yok

def analyze_verilog_file(file_path, module_type):
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return None

    with open(file_path, "r") as f:
        verilog_code = f.read()

    metrics = {
        "fluency": calculate_fluency(verilog_code),
        "flexibility": calculate_flexibility(verilog_code),
        "originality": calculate_originality(verilog_code, module_type),
        "elaboration": calculate_elaboration(verilog_code)
    }

    metrics["creativity_score"] = sum(metrics.values()) / len(metrics)
    return metrics

def calculate_functionality(verilog_code_path, testbench_path):
    """
    Verilog kodunun fonksiyonelliğini test ederek skor döndürür.
    """
    functionality_score = test_verilog_code(verilog_code_path, testbench_path)
    return functionality_score


if __name__ == "__main__":
    available_modules = {
        "1": ("models/adder_code_1.v", "adder"),
        "2": ("models/adder_code_2.v", "adder"),
        "3": ("models/adder_code_3.v", "adder"),
        "4": ("models/mux_code_1.v", "mux"),
        "5": ("models/mux_code_2.v", "mux"),
        "6": ("models/mux_code_3.v", "mux"),
        "7": ("models/generated_code_gpt_neo_1.3B.v", "adder")
    }

    print("Analiz edilecek modülleri seçin (örn: 1 3 4):")
    for key, value in available_modules.items():
        print(f"{key}. {value[0]}")

    selected_keys = input("Seçimlerinizi boşlukla ayırarak girin: ").split()
    selected_modules = [available_modules[key] for key in selected_keys if key in available_modules]

    if not selected_modules:
        print("Geçerli bir seçim yapılmadı. Program sonlandırılıyor.")
        exit()

    # Sonuç dosyasını kaydetmek için kullanıcıdan isim al
    result_filename = input("Sonuç dosyası adı (örnek: analysis_results.csv): ")

    results = []
    for file_path, module_type in selected_modules:
        print(f"Analyzing {file_path}...")
        metrics = analyze_verilog_file(file_path, module_type)
        metrics["file_name"] = file_path
        results.append(metrics)

    # Sonuçları bir DataFrame'e dönüştürüp göster
    df = pd.DataFrame(results, columns=["file_name", "fluency", "flexibility", "originality", "elaboration", "creativity_score"])
    print("\nAnalysis Results:")
    print(df)

    # Sonuçları CSV olarak kaydet
    df.to_csv(f"data/{result_filename}", index=False)
    print(f"\nResults saved to data/{result_filename}")
