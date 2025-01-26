from difflib import SequenceMatcher
import os
import pandas as pd
from scripts.test_verilog import test_verilog_code

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
    "fluency": float(calculate_fluency(verilog_code)),
    "flexibility": float(calculate_flexibility(verilog_code)),
    "originality": float(calculate_originality(verilog_code, module_type)),
    "elaboration": float(calculate_elaboration(verilog_code)),
    "functionality": float(calculate_functionality(file_path, f"prompts/{module_type}_testbench.v"))
    }

    print("Metrics Content:", metrics)

    metrics["creativity_score"] = calculate_creativity_score(metrics)
    return metrics

def calculate_functionality(verilog_code_path, testbench_path):
    test_output = test_verilog_code(verilog_code_path, testbench_path)
    return test_output  

def calculate_creativity_score(metrics):
    weights = {
        "fluency": 0.15,
        "flexibility": 0.15,
        "originality": 0.15,
        "elaboration": 0.15,
        "functionality": 0.40
    }
    score = sum(float(metrics[key]) * weights[key] for key in weights)
    return score


