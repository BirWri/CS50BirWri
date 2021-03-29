import os
from flask import Flask, flash, g,  request, redirect, url_for, send_from_directory, Blueprint, render_template, current_app
from werkzeug.utils import secure_filename
from flask import current_app
from flaskr.db import get_db

import cv2
import numpy as np
from PIL import Image, ImageFilter, ImageOps


from config import ALLOWED_EXTENSIONS, UPLOAD_FOLDER
from helpers import get_image

import sqlite3

bp = Blueprint('upload', __name__)

#i can remove this and import from helpers
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@bp.route('/upload', methods=['GET', 'POST'])
def upload_file():
    
    if request.method == 'POST':

        cartoon_title = request.form['title']
        file = request.files['file']
        
        
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            # where does rediredt take me?
            return redirect(request.url)
        
        
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            # save the file to the folder
            file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))

            #https://pynative.com/python-sqlite-blob-insert-and-retrieve-digital-data/
            # the path to the saved file from above
            photoPath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)

            # convert photo to blob, so i can store it in db as a blob
            def convertToBinaryData(klup):
            # Convert digital data to binary format
                with open(photoPath, 'rb') as file:
                    blobData = file.read()
                return blobData 

            cartoon_original_photo = convertToBinaryData(photoPath)

            #rename the filename to be the user choisen cartoon image title
            # POINTLESS??
            #cartoon_original_image = filename

            #save the original image path in db
            db = get_db()
            db.execute(
                'INSERT INTO cartoon ( cartoon_title, cartoon_author_id, cartoon_original_image, cartoon_original_photo)'
                ' VALUES (?, ?, ?, ?)',
                (cartoon_title, g.user['user_id'],  filename, cartoon_original_photo)
            )
            db.commit()
            return redirect(url_for('upload.uploaded_file', cartoon_title=cartoon_title))
    else:                                
        return render_template('upload/upload.html')

@bp.route('/upload/<cartoon_title>')
def uploaded_file(cartoon_title):

    #I use the db data to edit a photo, but it can be done much easier by just having the path to the photo instead of converting a blob to jpeg again...
    entry = get_image(cartoon_title)
    # The blob column from db
    data = entry[5]
    
    photoPath = current_app.config['UPLOAD_FOLDER'] + cartoon_title + ".jpg"

    print("BITCH HERE")
    print(photoPath)

    def writeTofile(data, cartoon_title):
    # Convert binary data to proper format and write it on Hard Disk
        with open(cartoon_title, 'wb') as file:
            file.write(data)
    
    writeTofile(data, photoPath)
    
    before2= Image.open(photoPath)
    

    #before = response(current_app.config['UPLOAD_FOLDER'], entry[4])
    edgeEnahnced = before2.filter(ImageFilter.EDGE_ENHANCE)
    gray = ImageOps.grayscale(before2)
    color2 = before2.quantize(9)

    color2=color2.convert('RGB')
    
    new_name= cartoon_title + ".jpg"

    color2.save(os.path.join(current_app.config['UPLOAD_FOLDER'], new_name))

    db = get_db()

    db.execute(
                'UPDATE cartoon SET cartoon_image_name=? WHERE cartoon_author_id=? AND cartoon_title =? ',
                (cartoon_title, g.user['user_id'], cartoon_title)
            )
    db.commit()
    
    

    return send_from_directory(current_app.config['UPLOAD_FOLDER'],
                               new_name)