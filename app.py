import os
import PyPDF2
from flask import Flask, request, redirect, url_for
from werkzeug.utils import secure_filename

os.system("mkdir files")
UPLOAD_FOLDER = os.popen("pwd").read().strip() + "/files"
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def read_data(filename):
    pdfFileObj = open('files/' + filename, 'rb')
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
    number_of_pages = pdfReader.getNumPages()
    for page_number in range(number_of_pages): 
        page = pdfReader.getPage(page_number).extractText().split(" ")  
        

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file',
                                    filename=filename))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''

from flask import send_from_directory

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    read_data(filename)
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)

if __name__ == "__main__":
    app.run()
