from flask import Flask, render_template, request, send_file
import yt_dlp
import os
import zipfile

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form['url']
        # ডাউনলোড ফোল্ডার
        if not os.path.exists('downloads'): os.makedirs('downloads')
        
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3', 'preferredquality': '192'}],
            'outtmpl': 'downloads/%(title)s.%(ext)s',
            'ignoreerrors': True,
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
            
        # সব ফাইল জিপ করা
        zip_filename = "music_collection.zip"
        with zipfile.ZipFile(zip_filename, 'w') as zipf:
            for file in os.listdir('downloads'):
                zipf.write(os.path.join('downloads', file), file)
        
        return send_file(zip_filename, as_attachment=True)
        
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)