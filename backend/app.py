from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import re

app = Flask(__name__)
CORS(app)


@app.route('/')
def home():
    return jsonify({
        'message': '실시간 음성 인식 API',
        'version': '1.0.0',
        'endpoints': {
            'POST /process_text': '텍스트 분석',
            'GET /health': '서버 상태 확인'
        }
    })


@app.route('/process_text', methods=['POST'])
def process_text():
    try:
        data = request.get_json()

        if 'text' not in data:
            return jsonify({'error': 'No text provided'}), 400

        text = data['text'].strip()

        # 간단한 텍스트 처리 (예: 단어 수, 문자 수 등)
        word_count = len(text.split())
        char_count = len(text)
        sentence_count = len(re.findall(r'[.!?]+', text))

        return jsonify({
            'success': True,
            'original_text': text,
            'processed_text': text.upper(),  # 예시: 대문자 변환
            'statistics': {
                'word_count': word_count,
                'char_count': char_count,
                'sentence_count': sentence_count
            }
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/health')
def health():
    return jsonify({'status': 'healthy', 'service': 'voice-recognition-api'})


if __name__ == '__main__':
    app.run(debug=True, port=5000)
