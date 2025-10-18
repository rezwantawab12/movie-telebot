from flask import Flask, send_from_directory, render_template_string
import os

app = Flask(__name__)

# مسیر پوشه‌ای که فایل‌ها داخلش هستند
UPLOAD_FOLDER = "/home/rezwan/uploads"

@app.route("/")
def index():
    # لیست تمام فایل‌ها داخل پوشه
    files = os.listdir(UPLOAD_FOLDER)
    # ساختن HTML داینامیک برای نمایش فایل‌ها
    file_links = ""
    for f in files:
        file_links += f'<li><a href="/download/{f}">{f}</a></li>'
    
    html = f'''
        <h1>Files available for download</h1>
        <ul>
            {file_links}
        </ul>
    '''
    return render_template_string(html)

@app.route("/download/<filename>")
def download_file(filename):
    # بررسی اینکه فایل واقعا وجود دارد
    if os.path.exists(os.path.join(UPLOAD_FOLDER, filename)):
        return send_from_directory(UPLOAD_FOLDER, filename, as_attachment=True)
    else:
        return f"<h2>File '{filename}' not found!</h2>", 404

if __name__ == "__main__":
    app.run(host="127.0.0.1" , port="80" ,debug=True)
