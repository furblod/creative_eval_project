from flask import Flask, render_template, request, redirect, url_for, flash
import os
import subprocess
from analyze_verilog import analyze_verilog_file
import pandas as pd
from transformers import AutoModelForCausalLM, AutoTokenizer

app = Flask(__name__)
app.secret_key = "supersecretkey"

UPLOAD_FOLDER = 'models'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# Ana sayfa
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if 'verilog_file' not in request.files:
            return redirect(request.url)
        file = request.files['verilog_file']
        if file.filename == '':
            return redirect(request.url)
        if file:
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(file_path)
            return redirect(url_for('index'))

    files = os.listdir(app.config['UPLOAD_FOLDER'])
    return render_template("index.html", files=files)

# Analiz sayfası
@app.route("/analyze/<filename>")
def analyze(filename):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    module_type = "adder" if "adder" in filename else "mux"
    result = analyze_verilog_file(file_path, module_type)

    if not result:
        flash("Dosya analiz edilemedi.", "danger")
        return redirect(url_for("index"))

    df = pd.DataFrame([result])

    tables = [df.to_html(classes="table table-striped", index=False)]

    return render_template("analysis.html", filename=filename, tables=tables, result=result)


# Test sayfası
@app.route("/test/<filename>")
def test(filename):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    testbench_path = f"testbench/{'adder' if 'adder' in filename else 'mux'}_testbench.v"

    compile_command = ["iverilog", "-o", "simulation", file_path, testbench_path]
    run_command = ["vvp", "simulation"]

    compile_result = subprocess.run(compile_command, capture_output=True, text=True)
    
    if compile_result.returncode != 0:
        test_output = f"Compilation Error:\n{compile_result.stderr}"
    else:
        run_result = subprocess.run(run_command, capture_output=True, text=True)
        test_output = run_result.stdout

    return render_template("test.html", filename=filename, test_output=test_output)

# Verilog kod üretme sayfası
@app.route("/generate", methods=["GET", "POST"])
def generate():
    if request.method == "POST":
        model_name = request.form['model']
        prompt = request.form['prompt']
        filename = request.form['filename']

        if not filename.endswith(".v"):
            filename += ".v"

        if model_name == "gpt-neo-1.3B":
            model_path = "EleutherAI/gpt-neo-1.3B"
        elif model_name == "microsoft-phi-1":
            model_path = "microsoft/phi-1"
        else:
            flash("Geçersiz model seçimi!")
            return redirect(url_for("generate"))

        try:
            tokenizer = AutoTokenizer.from_pretrained(model_path)
            model = AutoModelForCausalLM.from_pretrained(model_path)

            inputs = tokenizer(prompt, return_tensors="pt")
            outputs = model.generate(**inputs, max_new_tokens=300)
            response = tokenizer.decode(outputs[0], skip_special_tokens=True)

            if "module" in response and "endmodule" in response:
                start_index = response.find("module")
                end_index = response.find("endmodule") + len("endmodule")
                filtered_code = response[start_index:end_index]
            else:
                filtered_code = "Geçerli Verilog kodu bulunamadı."

            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            with open(file_path, "w") as f:
                f.write(filtered_code)

            flash(f"Verilog kodu başarıyla {filename} olarak kaydedildi!")
            return redirect(url_for("index"))

        except Exception as e:
            flash(f"Hata: {str(e)}")
            return redirect(url_for("generate"))

    return render_template("generate.html")

@app.route("/delete/<filename>", methods=["POST"])
def delete(filename):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if os.path.exists(file_path):
        os.remove(file_path)
        flash(f"{filename} başarıyla silindi!", "success")
    else:
        flash(f"{filename} bulunamadı!", "danger")
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)

