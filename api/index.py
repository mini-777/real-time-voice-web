from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
import json
import re

app = Flask(__name__)
CORS(app)


@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)


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
    return jsonify({'status': 'healthy', 'service': 'voice-recognition'})


# HTML 템플릿 (React 앱)
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>실시간 음성 인식</title>
    <script src="https://unpkg.com/react@18/umd/react.development.js"></script>
    <script src="https://unpkg.com/react-dom@18/umd/react-dom.development.js"></script>
    <script src="https://unpkg.com/@babel/standalone/babel.min.js"></script>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        
        .container {
            background: white;
            border-radius: 20px;
            padding: 2rem;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            max-width: 700px;
            width: 90%;
            text-align: center;
        }
        
        h1 {
            color: #333;
            margin-bottom: 2rem;
            font-size: 2.5rem;
            font-weight: 300;
        }
        
        .record-button {
            background: linear-gradient(45deg, #ff6b6b, #ee5a24);
            border: none;
            border-radius: 50%;
            width: 120px;
            height: 120px;
            color: white;
            font-size: 1.2rem;
            cursor: pointer;
            transition: all 0.3s ease;
            margin: 2rem 0;
            box-shadow: 0 10px 30px rgba(255, 107, 107, 0.3);
        }
        
        .record-button:hover {
            transform: translateY(-5px);
            box-shadow: 0 15px 40px rgba(255, 107, 107, 0.4);
        }
        
        .record-button.recording {
            background: linear-gradient(45deg, #ff4757, #c44569);
            animation: pulse 1.5s infinite;
        }
        
        .record-button:disabled {
            opacity: 0.6;
            cursor: not-allowed;
        }
        
        @keyframes pulse {
            0% { transform: scale(1); }
            50% { transform: scale(1.05); }
            100% { transform: scale(1); }
        }
        
        .status {
            margin: 1rem 0;
            font-size: 1.1rem;
            color: #666;
        }
        
        .transcript {
            background: #f8f9fa;
            border-radius: 10px;
            padding: 1.5rem;
            margin: 2rem 0;
            min-height: 100px;
            border-left: 4px solid #667eea;
            text-align: left;
        }
        
        .transcript-text {
            font-size: 1.1rem;
            line-height: 1.6;
            color: #333;
            margin-bottom: 1rem;
        }
        
        .statistics {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
            gap: 1rem;
            margin-top: 1rem;
        }
        
        .stat-item {
            background: #e9ecef;
            padding: 0.5rem;
            border-radius: 8px;
            text-align: center;
        }
        
        .stat-number {
            font-size: 1.5rem;
            font-weight: bold;
            color: #667eea;
        }
        
        .stat-label {
            font-size: 0.9rem;
            color: #666;
        }
        
        .loading {
            display: inline-block;
            width: 20px;
            height: 20px;
            border: 3px solid #f3f3f3;
            border-top: 3px solid #667eea;
            border-radius: 50%;
            animation: spin 1s linear infinite;
        }
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        
        .error {
            color: #ff4757;
            background: #ffe3e3;
            padding: 1rem;
            border-radius: 8px;
            margin: 1rem 0;
        }
        
        .language-select {
            margin: 1rem 0;
        }
        
        .language-select select {
            padding: 0.5rem 1rem;
            border-radius: 8px;
            border: 2px solid #ddd;
            font-size: 1rem;
            background: white;
        }
        
        .controls {
            display: flex;
            gap: 1rem;
            justify-content: center;
            align-items: center;
            flex-wrap: wrap;
            margin: 1rem 0;
        }
        
        .clear-button {
            background: #6c757d;
            color: white;
            border: none;
            padding: 0.5rem 1rem;
            border-radius: 8px;
            cursor: pointer;
            transition: background 0.3s ease;
        }
        
        .clear-button:hover {
            background: #5a6268;
        }
    </style>
</head>
<body>
    <div id="root"></div>

    <script type="text/babel">
        const { useState, useRef, useEffect } = React;

        function VoiceRecognitionApp() {
            const [isRecording, setIsRecording] = useState(false);
            const [transcript, setTranscript] = useState('');
            const [processedText, setProcessedText] = useState('');
            const [statistics, setStatistics] = useState(null);
            const [status, setStatus] = useState('음성 인식을 시작하려면 버튼을 클릭하세요');
            const [isProcessing, setIsProcessing] = useState(false);
            const [error, setError] = useState('');
            const [language, setLanguage] = useState('ko-KR');
            const [isSupported, setIsSupported] = useState(true);
            
            const recognitionRef = useRef(null);

            useEffect(() => {
                // Web Speech API 지원 확인
                if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
                    setIsSupported(false);
                    setError('이 브라우저는 음성 인식을 지원하지 않습니다. Chrome 브라우저를 사용해주세요.');
                    return;
                }

                const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
                recognitionRef.current = new SpeechRecognition();
                
                const recognition = recognitionRef.current;
                recognition.continuous = true;
                recognition.interimResults = true;
                recognition.lang = language;

                recognition.onstart = () => {
                    setIsRecording(true);
                    setStatus('음성을 듣고 있습니다... 말씀해주세요');
                    setError('');
                };

                recognition.onresult = (event) => {
                    let finalTranscript = '';
                    let interimTranscript = '';

                    for (let i = event.resultIndex; i < event.results.length; i++) {
                        const transcript = event.results[i][0].transcript;
                        if (event.results[i].isFinal) {
                            finalTranscript += transcript;
                        } else {
                            interimTranscript += transcript;
                        }
                    }

                    setTranscript(finalTranscript + interimTranscript);
                    
                    if (finalTranscript) {
                        processText(finalTranscript);
                    }
                };

                recognition.onerror = (event) => {
                    setError(`음성 인식 오류: ${event.error}`);
                    setIsRecording(false);
                    setStatus('오류가 발생했습니다');
                };

                recognition.onend = () => {
                    setIsRecording(false);
                    setStatus('음성 인식이 중지되었습니다');
                };

                return () => {
                    if (recognition) {
                        recognition.stop();
                    }
                };
            }, [language]);

            const processText = async (text) => {
                if (!text.trim()) return;
                
                setIsProcessing(true);
                try {
                    const response = await fetch('/process_text', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({ text: text })
                    });
                    
                    const result = await response.json();
                    
                    if (result.success) {
                        setProcessedText(result.processed_text);
                        setStatistics(result.statistics);
                    } else {
                        setError(result.error || '텍스트 처리에 실패했습니다.');
                    }
                } catch (err) {
                    setError('서버 통신 중 오류가 발생했습니다.');
                    console.error('Error processing text:', err);
                } finally {
                    setIsProcessing(false);
                }
            };

            const startRecording = () => {
                if (!isSupported || !recognitionRef.current) return;
                
                setError('');
                setTranscript('');
                setProcessedText('');
                setStatistics(null);
                
                recognitionRef.current.lang = language;
                recognitionRef.current.start();
            };

            const stopRecording = () => {
                if (recognitionRef.current) {
                    recognitionRef.current.stop();
                }
            };

            const handleRecordClick = () => {
                if (isRecording) {
                    stopRecording();
                } else {
                    startRecording();
                }
            };

            const clearTranscript = () => {
                setTranscript('');
                setProcessedText('');
                setStatistics(null);
                setStatus('음성 인식을 시작하려면 버튼을 클릭하세요');
            };

            if (!isSupported) {
                return (
                    <div className="container">
                        <h1>🎤 실시간 음성 인식</h1>
                        <div className="error">
                            ❌ 이 브라우저는 음성 인식을 지원하지 않습니다.<br/>
                            Chrome, Edge, Safari 등의 최신 브라우저를 사용해주세요.
                        </div>
                    </div>
                );
            }

            return (
                <div className="container">
                    <h1>🎤 실시간 음성 인식</h1>
                    
                    <div className="language-select">
                        <label>언어 선택: </label>
                        <select 
                            value={language} 
                            onChange={(e) => setLanguage(e.target.value)}
                            disabled={isRecording}
                        >
                            <option value="ko-KR">한국어</option>
                            <option value="en-US">English (US)</option>
                            <option value="ja-JP">日本語</option>
                            <option value="zh-CN">中文 (简体)</option>
                            <option value="es-ES">Español</option>
                            <option value="fr-FR">Français</option>
                        </select>
                    </div>
                    
                    <div className="controls">
                        <button 
                            className={`record-button ${isRecording ? 'recording' : ''}`}
                            onClick={handleRecordClick}
                            disabled={!isSupported}
                        >
                            {isRecording ? '⏹️ 중지' : '🎤 시작'}
                        </button>
                        
                        <button 
                            className="clear-button"
                            onClick={clearTranscript}
                            disabled={isRecording}
                        >
                            🗑️ 지우기
                        </button>
                    </div>
                    
                    <div className="status">
                        {status}
                        {isProcessing && <span> <div className="loading"></div></span>}
                    </div>
                    
                    {error && (
                        <div className="error">
                            ❌ {error}
                        </div>
                    )}
                    
                    <div className="transcript">
                        <div className="transcript-text">
                            <strong>인식된 텍스트:</strong><br/>
                            {transcript || '여기에 인식된 텍스트가 표시됩니다...'}
                        </div>
                        
                        {processedText && (
                            <div className="transcript-text">
                                <strong>처리된 텍스트:</strong><br/>
                                {processedText}
                            </div>
                        )}
                        
                        {statistics && (
                            <div className="statistics">
                                <div className="stat-item">
                                    <div className="stat-number">{statistics.word_count}</div>
                                    <div className="stat-label">단어</div>
                                </div>
                                <div className="stat-item">
                                    <div className="stat-number">{statistics.char_count}</div>
                                    <div className="stat-label">문자</div>
                                </div>
                                <div className="stat-item">
                                    <div className="stat-number">{statistics.sentence_count}</div>
                                    <div className="stat-label">문장</div>
                                </div>
                            </div>
                        )}
                    </div>
                </div>
            );
        }

        ReactDOM.render(<VoiceRecognitionApp />, document.getElementById('root'));
    </script>
</body>
</html>
'''
