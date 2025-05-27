import React, { useState, useRef, useEffect } from 'react';
import axios from 'axios';
import './App.css';

// Web Speech API 타입 정의
declare global {
  interface Window {
    SpeechRecognition: any;
    webkitSpeechRecognition: any;
  }
}

interface Statistics {
  word_count: number;
  char_count: number;
  sentence_count: number;
}

const App: React.FC = () => {
  const [isRecording, setIsRecording] = useState(false);
  const [transcript, setTranscript] = useState('');
  const [processedText, setProcessedText] = useState('');
  const [statistics, setStatistics] = useState<Statistics | null>(null);
  const [status, setStatus] = useState(
    '음성 인식을 시작하려면 버튼을 클릭하세요'
  );
  const [isProcessing, setIsProcessing] = useState(false);
  const [error, setError] = useState('');
  const [language, setLanguage] = useState('ko-KR');
  const [isSupported, setIsSupported] = useState(true);

  const recognitionRef = useRef<any>(null);

  // API 기본 URL (개발 환경에서는 Flask 서버)
  const API_BASE_URL =
    process.env.NODE_ENV === 'production' ? '/api' : 'http://localhost:5000';

  useEffect(() => {
    // Web Speech API 지원 확인
    if (
      !('webkitSpeechRecognition' in window) &&
      !('SpeechRecognition' in window)
    ) {
      setIsSupported(false);
      setError(
        '이 브라우저는 음성 인식을 지원하지 않습니다. Chrome 브라우저를 사용해주세요.'
      );
      return;
    }

    const SpeechRecognition =
      window.SpeechRecognition || window.webkitSpeechRecognition;
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

    recognition.onresult = (event: any) => {
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

    recognition.onerror = (event: any) => {
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

  const processText = async (text: string) => {
    if (!text.trim()) return;

    setIsProcessing(true);
    try {
      const response = await axios.post(`${API_BASE_URL}/process_text`, {
        text: text,
      });

      const result = response.data;

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
      <div className='container'>
        <h1>🎤 실시간 음성 인식</h1>
        <div className='error'>
          ❌ 이 브라우저는 음성 인식을 지원하지 않습니다.
          <br />
          Chrome, Edge, Safari 등의 최신 브라우저를 사용해주세요.
        </div>
      </div>
    );
  }

  return (
    <div className='container'>
      <h1>🎤 실시간 음성 인식</h1>

      <div className='language-select'>
        <label>언어 선택: </label>
        <select
          value={language}
          onChange={(e) => setLanguage(e.target.value)}
          disabled={isRecording}
        >
          <option value='ko-KR'>한국어</option>
          <option value='en-US'>English (US)</option>
          <option value='ja-JP'>日本語</option>
          <option value='zh-CN'>中文 (简体)</option>
          <option value='es-ES'>Español</option>
          <option value='fr-FR'>Français</option>
        </select>
      </div>

      <div className='controls'>
        <button
          className={`record-button ${isRecording ? 'recording' : ''}`}
          onClick={handleRecordClick}
          disabled={!isSupported}
        >
          {isRecording ? '⏹️ 중지' : '🎤 시작'}
        </button>

        <button
          className='clear-button'
          onClick={clearTranscript}
          disabled={isRecording}
        >
          🗑️ 지우기
        </button>
      </div>

      <div className='status'>
        {status}
        {isProcessing && (
          <span>
            {' '}
            <div className='loading'></div>
          </span>
        )}
      </div>

      {error && <div className='error'>❌ {error}</div>}

      <div className='transcript'>
        <div className='transcript-text'>
          <strong>인식된 텍스트:</strong>
          <br />
          {transcript || '여기에 인식된 텍스트가 표시됩니다...'}
        </div>

        {processedText && (
          <div className='transcript-text'>
            <strong>처리된 텍스트:</strong>
            <br />
            {processedText}
          </div>
        )}

        {statistics && (
          <div className='statistics'>
            <div className='stat-item'>
              <div className='stat-number'>{statistics.word_count}</div>
              <div className='stat-label'>단어</div>
            </div>
            <div className='stat-item'>
              <div className='stat-number'>{statistics.char_count}</div>
              <div className='stat-label'>문자</div>
            </div>
            <div className='stat-item'>
              <div className='stat-number'>{statistics.sentence_count}</div>
              <div className='stat-label'>문장</div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default App;
