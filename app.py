from flask import Flask, render_template, request, redirect, url_for
import os
import pandas as pd
from analyze_verilog import analyze_verilog_file

app = Flask(__name__)

# Yüklenen dosyalar için yükleme klasörü belirleme
UPLOAD_FOLDER = 'models'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ana sayfa (dosya yükleme ve listeleme)
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

# Dosya analizi ve sonuçların gösterilmesi
@app.route("/analyze/<filename>")
def analyze(filename):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    module_type = "adder" if "adder" in filename else "mux"
    result = analyze_verilog_file(file_path, module_type)

    df = pd.DataFrame([result])
    df.to_csv(f"data/{filename}_analysis.csv", index=False)

    return render_template("analysis.html", filename=filename, tables=[df.to_html(classes="table table-striped")])

if __name__ == "__main__":
    app.run(debug=True)