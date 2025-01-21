import subprocess
import os

def test_verilog_code(verilog_code_path, testbench_path):
    # Verilog kodunu derle
    compile_result = subprocess.run(
        ["iverilog", "-o", "simulation", verilog_code_path, testbench_path],
        capture_output=True, text=True
    )
    if compile_result.returncode != 0:
        print("Compilation Error:\n", compile_result.stderr)
        return False

    # Simülasyonu çalıştır
    simulation_result = subprocess.run(
        ["vvp", "simulation"],
        capture_output=True, text=True
    )
    if simulation_result.returncode != 0:
        print("Simulation Error:\n", simulation_result.stderr)
        return False

    # Simülasyon çıktılarını yazdır
    print("Simülasyon çıktısı:\n", simulation_result.stdout)
    return True

if __name__ == "__main__":
    # Dosya yollarını tanımlayın
    verilog_code_path = "models/adder_code_1.v"
    testbench_path = "prompts/adder_testbench.v"

    # Kodun testi
    if os.path.exists(verilog_code_path) and os.path.exists(testbench_path):
        success = test_verilog_code(verilog_code_path, testbench_path)
        if success:
            print("Verilog code passed all tests!")
        else:
            print("Verilog code failed the tests!")
    else:
        print("Required files not found. Make sure both the Verilog code and testbench exist.")
