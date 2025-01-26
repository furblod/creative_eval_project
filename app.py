from flask import Flask, render_template, request, redirect, url_for
import os
import subprocess
from analyze_verilog import analyze_verilog_file
from flask import Flask, render_template, request, redirect, url_for, flash
import pandas as pd


app = Flask(__name__)

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

    # Sonuçları DataFrame'e dönüştür
    df = pd.DataFrame([result])

    # Tabloyu HTML formatına çevir
    tables = [df.to_html(classes="table table-striped", index=False)]

    return render_template("analysis.html", filename=filename, tables=tables, result=result)


# Test sayfası
@app.route("/test/<filename>")
def test(filename):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    testbench_path = f"prompts/{'adder' if 'adder' in filename else 'mux'}_testbench.v"

    # Test işlemi
    compile_command = ["iverilog", "-o", "simulation", file_path, testbench_path]
    run_command = ["vvp", "simulation"]

    compile_result = subprocess.run(compile_command, capture_output=True, text=True)
    
    if compile_result.returncode != 0:
        test_output = f"Compilation Error:\n{compile_result.stderr}"
    else:
        run_result = subprocess.run(run_command, capture_output=True, text=True)
        test_output = run_result.stdout

    return render_template("test.html", filename=filename, test_output=test_output)

if __name__ == "__main__":
    app.run(debug=True)
