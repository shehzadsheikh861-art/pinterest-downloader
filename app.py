from flask import Flask, request, jsonify, send_file
import requests
import re
from io import BytesIO

app = Flask(__name__)

def extract_video_url(html):
    matches = re.findall(r'https://v\.pinimg\.com/[^"]+', html)
    return matches[0] if matches else None

@app.route('/')
def home():
    return open('index.html').read()

@app.route('/download', methods=['POST'])
def download():
    url = request.json.get('url')
    headers = {"User-Agent": "Mozilla/5.0"}
    res = requests.get(url, headers=headers)

    video_url = extract_video_url(res.text)

    if not video_url:
        return jsonify({"status": "error", "message": "Video not found"})

    video_res = requests.get(video_url, headers=headers)
    return send_file(
        BytesIO(video_res.content),
        mimetype='video/mp4',
        as_attachment=True,
        download_name='pinterest_video.mp4'
    )

if __name__ == '__main__':
    app.run(debug=True)
