from flask import Flask, render_template, request, send_from_directory, session
import os
import pandas as pd
import numpy as np
from commission import Merge
from werkzeug.utils import secure_filename
from werkzeug.datastructures import  FileStorage

UPLOAD_FOLDER =  r".\uploads"
YEAR = '2020'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'dljsaklqk24e21cjn!Ew@@dsa5'

@app.route('/', methods=['GET','POST'])
def index():
    if request.method == 'POST':
        quarter = int(request.form['quarter'])
        session['quarter'] = quarter
        return render_template('upload.html', quarter = quarter)
    
    return render_template('index.html')

@app.route('/upload', methods=['POST','GET'])
def upload_file():
    if request.method == 'POST':
        mon1 = request.files['mon1']
        mon1.save(os.path.join(app.config['UPLOAD_FOLDER'],mon1.filename))
        mon2 = request.files['mon2']
        mon2.save(os.path.join(app.config['UPLOAD_FOLDER'],mon2.filename))
        mon3 = request.files['mon3']
        mon3.save(os.path.join(app.config['UPLOAD_FOLDER'],mon3.filename))
        try:
            mon1 = pd.read_excel(os.path.join(app.config['UPLOAD_FOLDER'],mon1.filename), sheet_name='Commission Transactions', engine='openpyxl')          
        except:
            return "The first month file is not valid"
        try:
            mon2 = pd.read_excel(os.path.join(app.config['UPLOAD_FOLDER'],mon2.filename), sheet_name='Commission Transactions', engine='openpyxl')
        except:
            return "The second month file is not valid"
        try:
            mon3 = pd.read_excel(os.path.join(app.config['UPLOAD_FOLDER'],mon3.filename), sheet_name='Commission Transactions', engine='openpyxl')
        except:
            return "The thrid month file is not valid"
        
        merge = Merge()
        merge.begin(session.get("quarter"), mon1, mon2, mon3)
        report = 'Q' + str(session.get("quarter")) + '-' + YEAR +'-comm.xlsx'
        return render_template('download.html' , report = report)
    else:
        print('failed')
        return render_template('upload.html')

@app.route('/download')
def download_file():
    if request.method == 'GET':
        return send_from_directory(app.config['UPLOAD_FOLDER'], 'Q' + str(session.get("quarter")) + '-' + YEAR +'-comm.xlsx')


@app.route('/finish')
def finish_program():
    if request.method == 'GET':
        filelist = [ f for f in os.listdir(UPLOAD_FOLDER) if f.endswith(".xlsx") ]
        for f in filelist:
            os.remove(os.path.join(UPLOAD_FOLDER, f))
        return render_template('index.html')



if __name__ == "__main__":
    app.run(debug=True)