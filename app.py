from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

@app.route('/')
def index():
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)
    
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    
    if file:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)
        return redirect(url_for('analyze', filename=file.filename))

@app.route('/analyze/<filename>')
def analyze(filename):
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    df = pd.read_csv(filepath)
    analysis = {
        'shape': df.shape,
        'columns': df.columns.tolist(),
        'head': df.head().to_html(),
        'describe': df.describe().to_html(),
        'null_values': df.isnull().sum().to_dict(),
        'dtypes': df.dtypes.to_dict()
    }
    return render_template('analysis.html', analysis=analysis, filename=filename)

if __name__ == '__main__':
    app.run(debug=True)
