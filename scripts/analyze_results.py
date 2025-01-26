from difflib import SequenceMatcher
import os
import pandas as pd
from test_verilog import test_verilog_code

def calculate_fluency(verilog_code):
    required_keywords = ["module", "input", "output", "assign", "endmodule", "wire", "reg", "always", "begin", "end"]
    keyword_count = sum(1 for keyword in required_keywords if keyword in verilog_code)
    ratio = keyword_count / len(required_keywords)

    if ratio == 1.0:
        return 1.0
    elif ratio >= 0.8:
        return 0.8
    elif ratio >= 0.5:
        return 0.5
    elif ratio >= 0.2:
        return 0.2
    else:
        return 0.0

def calculate_flexibility(verilog_code):
    assign_count = verilog_code.count("assign")
    always_count = verilog_code.count("always")
    wire_count = verilog_code.count("wire")
    case_count = verilog_code.count("case")
    if_else_count = verilog_code.count("if") + verilog_code.count("else")

    score = 0.0
    if assign_count > 1:
        score += 0.5
    if always_count > 0 or wire_count > 0:
        score += 0.3
    if case_count > 0 or if_else_count > 0:
        score += 0.2

    if score >= 1.0:
        return 1.0
    elif score >= 0.8:
        return 0.8
    elif score >= 0.5:
        return 0.5
    elif score >= 0.2:
        return 0.2
    else:
        return 0.0

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

    if similarity < 0.5:
        return 1.0
    elif similarity < 0.7:
        return 0.8
    elif similarity < 0.85:
        return 0.5
    elif similarity < 0.95:
        return 0.2
    else:
        return 0.0

def calculate_elaboration(verilog_code):
    comments = [line for line in verilog_code.splitlines() if "//" in line or "/*" in line]
    comment_ratio = len(comments) / len(verilog_code.splitlines()) if verilog_code.splitlines() else 0.0

    if comment_ratio > 0.3:
        return 1.0
    elif comment_ratio > 0.2:
        return 0.8
    elif comment_ratio > 0.1:
        return 0.5
    elif comment_ratio > 0.05:
        return 0.2
    else:
        return 0.0

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
        "elaboration": calculate_elaboration(verilog_code),
        "functionality": calculate_functionality(file_path, f"prompts/{module_type}_testbench.v")
    }

    metrics["creativity_score"] = calculate_creativity_score(metrics)
    return metrics

def calculate_functionality(verilog_code_path, testbench_path):
    functionality_score = test_verilog_code(verilog_code_path, testbench_path)
    return functionality_score

def calculate_creativity_score(metrics):
    weights = {
        "fluency": 0.15,
        "flexibility": 0.15,
        "originality": 0.15,
        "elaboration": 0.15,
        "functionality": 0.40
    }
    score = sum(metrics[key] * weights[key] for key in weights)
    return score

if __name__ == "__main__":
    available_modules = {
        "1": ("models/adder_code_1.v", "adder"),
        "2": ("models/adder_code_2.v", "adder"),
        "3": ("models/adder_code_3.v", "adder"),
        "4": ("models/mux_code_1.v", "mux"),
        "5": ("models/mux_code_2.v", "mux"),
        "6": ("models/mux_code_3.v", "mux"),
        "7": ("models/adder_code_gpt_neo_1.3B.v", "adder"),
        "8": ("models/adder_code_phi1.v", "adder")
    }

    print("Analiz edilecek modülleri seçin (örneğin: 1 3 4):")
    for key, value in available_modules.items():
        print(f"{key}. {value[0]}")

    selected_keys = input("Seçimlerinizi boşlukla ayırarak girin: ").split()
    selected_modules = [available_modules[key] for key in selected_keys if key in available_modules]

    if not selected_modules:
        print("Geçerli bir seçim yapılmadı. Program sonlandırılıyor.")
        exit()

    result_filename = input("Sonuç dosyası adı (örnek: analysis_results.csv): ")

    results = []
    for file_path, module_type in selected_modules:
        print(f"{file_path} Analiz ediliyor...")
        metrics = analyze_verilog_file(file_path, module_type)
        metrics["functionality"] = calculate_functionality(file_path, f"prompts/{module_type}_testbench.v")
        metrics["file_name"] = file_path
        results.append(metrics)

    df = pd.DataFrame(results, columns=["file_name", "fluency", "flexibility", "originality", "elaboration", "functionality", "creativity_score"])
    print("\nAnaliz Sonuçları:")
    print(df)

    df.to_csv(f"data/{result_filename}", index=False)
    print(f"\nSonuçlar dosyaya kaydedildi: data/{result_filename}")
