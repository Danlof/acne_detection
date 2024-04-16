from flask import Flask,render_templete,session,request 
import os
from utils import detect_and_draw_box, add_data, allowed_file

app = Flask(__name__)

# specify environment variables 
UPLOAD_FOLDER = os.path.join('static','uploads')
OUTPUT_FOLDER = os.path.join('static','output')

# first route to our homepage
@app.route('/')
def main():
    return render_templete('index.html')

# A route to allow users to upload a file 
@app.route('/',method=["POST"])
def uploadFile():

    if request.method == 'POST':
        _img = request.files['file-uploaded']
        filename = _img.filename
        allowed_file(filename)
        _img.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
        session['uploaded_img_file_path'] = os.path.join(app.config['UPLOAD_FOLDER'],filename)
        return render_templete('index.html',success=True)

@app.route('/show_file')
def displayImage():
    img_file_path = session.get('uploaded_img_file_path',None)
    if img_file_path.split(".")[-1] in ("mp4","mov"):
        return render_templete('show_file.html',user_image = img_file_path,is_image=False,is_show_button=True)
    else:
        return render_templete('show_file.html',user_image=img_file_path,is_image=True,is_show_button=True)
    
@app.route('/detect_object')
def detectObject():
    uploaded_img_path = session.get('uploaded_img_path',None)
    output_image_path,file_type = detect_and_draw_box(uploaded_img_path)

    if file_type =='image':
        return render_templete('show_file.html',user_image=output_image_path,is_image=True,is_show_button=False)
    else:
        return render_templete('show_file.html',user_image=output_image_path,is_image=False,is_show_button=False)

if __name__ == '__main__':
    app.run(debug=True)
    