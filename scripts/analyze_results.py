from difflib import SequenceMatcher
import os
import pandas as pd

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

if __name__ == "__main__":
    # Analiz edilecek Verilog dosyaları ve ilgili modül türleri
    verilog_files = [
        ("models/adder_code_1.v", "adder"),
        ("models/adder_code_2.v", "adder"),
        ("models/adder_code_3.v", "adder"),
        ("models/mux_code_1.v", "mux"),
        ("models/mux_code_2.v", "mux"),
        ("models/mux_code_3.v", "mux")
    ]

    results = []
    for file_path, module_type in verilog_files:
        print(f"Analyzing {file_path} as {module_type}...")
        metrics = analyze_verilog_file(file_path, module_type)
        if metrics:
            metrics["file_name"] = file_path
            results.append(metrics)

    # Sonuçları bir DataFrame'e dönüştürüp göster
    import pandas as pd
    df = pd.DataFrame(results, columns=["file_name", "fluency", "flexibility", "originality", "elaboration", "creativity_score"])
    print("Analysis Results:")
    print(df)

    # Sonuçları CSV olarak kaydet
    df.to_csv("data/results_analysis.csv", index=False)
    print("\nResults saved to 'data/results_analysis.csv'.")