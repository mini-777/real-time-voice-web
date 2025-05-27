# 🎤 실시간 음성 인식 앱 (Flask + React + Web Speech API)

브라우저의 Web Speech API를 활용한 실시간 음성 인식 웹 애플리케이션입니다. Flask 백엔드와 React 프론트엔드로 구성되어 있으며, Vercel에서 서버리스 함수로 배포됩니다.

## ✨ 주요 기능

- 🎙️ **실시간 음성 인식**: 브라우저의 Web Speech API 사용
- 🌐 **다국어 지원**: 한국어, 영어, 일본어, 중국어, 스페인어, 프랑스어
- 📊 **텍스트 분석**: 단어 수, 문자 수, 문장 수 통계 제공
- 📱 **반응형 디자인**: 모바일과 데스크톱 모두 지원
- ⚡ **실시간 처리**: 즉시 음성을 텍스트로 변환

## 🛠️ 기술 스택

### 백엔드

- **Flask 3.0.3**: 웹 프레임워크
- **Flask-CORS**: CORS 지원

### 프론트엔드

- **React 18**: UI 라이브러리 (CDN)
- **Vanilla CSS**: 스타일링
- **Web Speech API**: 브라우저 내장 음성 인식

### 배포

- **Vercel**: 서버리스 배포 플랫폼
- **Python Runtime**: 서버리스 함수

## 🚀 로컬 실행

### 1. 의존성 설치

```bash
pip install -r requirements.txt
```

### 2. 개발 서버 실행

```bash
# Vercel CLI 설치 (처음 한 번만)
npm i -g vercel

# 개발 서버 시작
vercel dev
```

애플리케이션이 `http://localhost:3000`에서 실행됩니다.

## 📋 API 엔드포인트

### `POST /process_text`

텍스트를 받아 분석 결과를 반환합니다.

**요청 본문:**

```json
{
  "text": "분석할 텍스트"
}
```

**응답:**

```json
{
  "success": true,
  "original_text": "분석할 텍스트",
  "processed_text": "분석할 텍스트",
  "statistics": {
    "word_count": 2,
    "char_count": 7,
    "sentence_count": 0
  }
}
```

### `GET /health`

서버 상태를 확인합니다.

**응답:**

```json
{
  "status": "healthy",
  "service": "voice-recognition"
}
```

## 🎯 사용 방법

1. 웹 페이지에 접속
2. 언어 선택 (한국어, 영어 등)
3. 마이크 권한 허용
4. 🎤 시작 버튼 클릭하여 음성 인식 시작
5. 음성으로 말하기
6. ⏹️ 중지 버튼으로 종료
7. 인식된 텍스트와 통계 확인

## 📦 배포

### Vercel 배포

```bash
vercel --prod
```

또는 GitHub 연동을 통한 자동 배포를 설정할 수 있습니다.

## 🔒 보안 고려사항

- 음성 인식은 브라우저에서 직접 처리되어 서버로 전송되지 않습니다
- CORS가 활성화되어 있어 브라우저에서 안전하게 접근 가능합니다
- 마이크 권한은 사용자가 명시적으로 허용해야 합니다

## 🌐 브라우저 호환성

- **Chrome**: 완전 지원 ✅
- **Edge**: 완전 지원 ✅
- **Safari**: 부분 지원 ⚠️
- **Firefox**: 제한적 지원 ⚠️

**권장**: Chrome 또는 Edge 브라우저 사용

## 🐛 문제 해결

### 마이크 접근 오류

- HTTPS 환경에서만 마이크 접근이 가능합니다
- 브라우저 설정에서 마이크 권한을 확인하세요

### 음성 인식 오류

- 조용한 환경에서 명확하게 발음하세요
- 인터넷 연결 상태를 확인하세요
- Chrome 브라우저를 사용해보세요

### 배포 오류

```bash
# Vercel 재로그인
vercel logout
vercel login

# 다시 배포
vercel --prod
```

## 📄 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다.
