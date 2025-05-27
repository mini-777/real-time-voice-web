from flask import Flask, Response, request, jsonify
from flask_cors import CORS
import json
import re

app = Flask(__name__)
CORS(app)

HTML = r"""
<!DOCTYPE html>
<html lang='ko'>
<head>
<meta charset='UTF-8'>
<meta name='viewport' content='width=device-width, initial-scale=1.0'>
<title>실시간 음성 인식</title>
<script src='https://unpkg.com/react@18/umd/react.development.js'></script>
<script src='https://unpkg.com/react-dom@18/umd/react-dom.development.js'></script>
<script src='https://unpkg.com/@babel/standalone/babel.min.js'></script>
</head>
<body>
<div id='root'></div>
<script type='text/babel'>
function App(){return React.createElement('h1', {style: {textAlign:'center', marginTop:'40vh'}}, '🎤 실시간 음성 인식 서버 준비 완료!');}
ReactDOM.render(React.createElement(App),document.getElementById('root'));</script>
</body>
</html>
"""


@app.route('/', methods=['GET'])
def index():
    return Response(HTML, mimetype='text/html')


@app.route('/health')
def health():
    return jsonify({'status': 'ok'})

# Example API route for text processing (optional)


@app.route('/process_text', methods=['POST'])
def process_text():
    data = request.get_json(force=True)
    text = data.get('text', '')
    wc = len(text.split())
    return jsonify({'original': text, 'word_count': wc})
