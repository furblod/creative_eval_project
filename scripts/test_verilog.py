import subprocess

def test_verilog_code(verilog_code_path, testbench_path):

    compile_result = subprocess.run(
        ["iverilog", "-o", "simulation", verilog_code_path, testbench_path],
        capture_output=True, text=True
    )

    if compile_result.returncode != 0:
        print(f"Compilation Error in {verilog_code_path}:\n", compile_result.stderr)
        return 0.0 #Tüm tesler başarısız oldu

    simulation_result = subprocess.run(
        ["vvp", "simulation"],
        capture_output=True, text=True
    )

    print(f"\nTest Results for {verilog_code_path}:\n")
    print(simulation_result.stdout)

    output = simulation_result.stdout.lower()
    if "error" in output or "fail" in output:
        return 0.5  # Bazı testler başarısız oldu
    else:
        return 1.0  # Tüm testler başarıyla geçti

if __name__ == "__main__":
    available_modules = {
        "1": ("models/adder_code_1.v", "testbench/adder_testbench.v"),
        "2": ("models/adder_code_2.v", "testbench/adder_testbench.v"),
        "4": ("models/mux_code_1.v", "testbench/mux_testbench.v"),
        "5": ("models/mux_code_2.v", "testbench/mux_testbench.v"),
        "6": ("models/mux_code_3.v", "testbench/mux_testbench.v"),
        "7": ("models/generated_code_gpt_neo_1.3B.v", "testbench/adder_testbench.v"),
        "8": ("models/generated_code_phi1.v", "testbench/adder_testbench.v")
    }

    print("Test edilecek modülleri seçin (örn: 1 3 4):")
    for key, value in available_modules.items():
        print(f"{key}. {value[0]}")

    selected_keys = input("Seçimlerinizi boşlukla ayırarak girin: ").split()
    selected_modules = [available_modules[key] for key in selected_keys if key in available_modules]

    if not selected_modules:
        print("Geçerli bir seçim yapılmadı. Program sonlandırılıyor.")
        exit()

    # Sonuç dosyasını kaydetmek için kullanıcıdan isim al
    result_filename = input("Sonuç dosyası adı (örnek: test_results.csv): ")

    results = []
    for verilog_code_path, testbench_path in selected_modules:
        print(f"\nRunning tests for {verilog_code_path}...\n")
        functionality_score = test_verilog_code(verilog_code_path, testbench_path)
        results.append((verilog_code_path, functionality_score))

    # Sonuçları kaydet
    with open(f"data/{result_filename}", "w") as f:
        f.write("file_name,functionality\n")
        for file_name, score in results:
            f.write(f"{file_name},{score}\n")

    print(f"\nResults saved to data/{result_filename}")
