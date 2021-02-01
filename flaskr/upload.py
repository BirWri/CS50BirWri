import os
from flask import Flask, flash, g,  request, redirect, url_for, send_from_directory, Blueprint, render_template
from werkzeug.utils import secure_filename
from flask import current_app
from flaskr.db import get_db


from . import ALLOWED_EXTENSIONS, UPLOAD_FOLDER


bp = Blueprint('upload', __name__)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@bp.route('/upload', methods=['GET', 'POST'])
def upload_file():
    
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']

        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
            path_1 = UPLOAD_FOLDER+filename
            print(path_1)

            #save the path in db
            db = get_db()
            db.execute(
                'INSERT INTO canvas (uploader_id, path_1)'
                ' VALUES (?, ?)',
                (g.user['id'], path_1)
            )
            db.commit()
            #return redirect(url_for('uploaded_file',
                                    #filename=filename))
            return redirect("/")
    else:                                
        return render_template('upload/upload.html')

@bp.route('/upload/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)