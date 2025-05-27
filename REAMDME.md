# 프로젝트 리포트 : 실시간 음성 인식 웹 애플리케이션 (Flask + React)

## 1. 문제 정의

브라우저에서 마이크로 입력한 음성을 **실시간으로 텍스트로 변환**하고, 간단한 통계(단어·문자·문장 수)를 계산해 즉시 화면에 표시하는 웹 서비스를 구축한다. 서비스는 **Vercel** Python Serverless Functions 위에 배포되며 모든 사용자가 배포 URL 접속 시 곧바로 이용할 수 있어야 한다.

## 2. 요구사항 분석

| 분류 | 세부 내용                                                                                                                                             |
| ---- | ----------------------------------------------------------------------------------------------------------------------------------------------------- |
| 기능 | 1) 🎙️ 웹 페이지에서 마이크 녹음 <br>2) Web Speech API로 음성→텍스트 변환 <br>3) `/process_text` API로 텍스트 통계 계산 <br>4) 결과를 UI에 실시간 표출 |
| 동작 | • 다국어 지원(ko-KR, en-US 등) <br>• 루트 도메인 `/` 진입 시 화면 제공 <br>• `/health` 엔드포인트 제공                                                |
| 품질 | • Vercel 배포 후 404 / 500 오류 없음 <br>• CORS 허용 <br>• 모바일·데스크톱 반응형                                                                     |
| 제약 | • 백엔드: Flask (Serverless) <br>• 프론트엔드: React (CDN 로드) <br>• 별도 빌드 스텝 없이 배포                                                        |

## 3. 기술 스택 및 아키텍처 설명

```
┌────────────┐          HTTP(S)           ┌────────────┐
│   Client   │  ───────────────────────▶ │  Vercel    │
│ (Browser)  │                           │  Edge FN   │
└────────────┘ ◀───────────────────────  │  (Flask)   │
        ▲  Web Speech API    JSON △      └────────────┘
        │                          │
        └────────  React UI  ──────┘
```

- **Frontend** : React 18(Umd) + TypeScript + CSS – 브라우저에서 Web Speech API 사용.
- **Backend** : Flask 3 + flask-cors – `/`, `/health`, `/process_text` 를 제공.
- **Hosting** : Vercel (Serverless Functions, Python Runtime).
- **Routing** : `vercel.json` `rewrites` → 모든 경로를 `/api/index` 함수로 전달.

## 4. 핵심 알고리즘 및 처리 메커니즘 상세 설명

1. **음성 인식** : Web Speech API(`SpeechRecognition`, `webkitSpeechRecognition`)를 연속 모드로 실행하여 interim/final 결과를 수신.
2. **텍스트 처리** :`/process_text` POST ```python
   word_count = len(text.split())
   char_count = len(text)
   sentence_count = len(re.findall(r'[.!?]+', text))

````
3. **UI 업데이트** : React state ( `transcript`, `processedText`, `statistics` ) 를 실시간 갱신.

## 5. 구현 과정 및 주요 코드 설명
### 5-1 `api/index.py`
```python
app = Flask(__name__)
HTML = r"""<html>… React CDN …</html>"""
@app.route('/')
def index():
    return Response(HTML, mimetype='text/html')
````

• **Jinja 충돌 방지** : raw string + `Response` 로 그대로 HTML 전달.  
• `/process_text` : JSON 입력 → 통계 계산 → JSON 반환.

### 5-2 `vercel.json`

```json
{ "rewrites": [{ "source": "/(.*)", "destination": "/api/index" }] }
```

### 5-3 클라이언트(`frontend/src/App.tsx`)

- `recognition.onresult` 이벤트에서 final 문장을 감지해 API 호출.
- TypeScript interface `Statistics` 로 응답 타입을 명확히.

## 6. 해결 과정에서 발생한 문제점과 해결 방법

| 문제               | 증상                                  | 해결                                                                                                                          |
| ------------------ | ------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------- |
| 404 NOT FOUND      | 배포 후 루트 접속 404                 | `vercel.json` 삭제 → 복구하여 모든 경로를 함수에 리라이트                                                                     |
| 500 Internal Error | Jinja2 TemplateError                  | HTML의 `{{…}}` (JSX) 가 Jinja 변수로 해석 → JSX를 React.createElement 로 수정 & `render_template_string` → `Response` 로 변경 |
| `python` 명령 없음 | macOS zsh `command not found: python` | `python3` 사용 및 venv 안내                                                                                                   |
| CORS 차단          | 브라우저 fetch 실패                   | `flask-cors` 로 `CORS(app)` 활성화                                                                                            |

## 7. 습득한 기술 및 인사이트

- **Vercel Python Runtime** 의 서버리스 동작 방식과 디렉터리 구조 제약.
- **Jinja2-React 충돌** : `{{ }}` 중첩 시 템플릿 엔진이 먼저 해석하므로 raw HTML 전달 필요.
- **Web Speech API** 실전 사용법, interim / final 구분 로직.
- 간단한 수정 후 **빌드 없이** 서버리스 함수만 재배포해 빠르게 피드백 받을 수 있다는 점.

## 8. 결론 및 향후 개선 방향

현재 버전은 “서버 작동 여부 확인용” 페이지와 간단한 텍스트 통계 API 까지만 포함한다. 다음 단계는:

1. **완전한 React SPA** 를 별도 `build/` 폴더에 빌드하여 정적 배포 + API 프록시
2. **WebSocket** 으로 음성 인식 스트리밍(지연 최소화)
3. **Whisper API / 로컬 모델** 연동으로 인식 정확도 향상
4. **다국어 번역, 실시간 자막** 등 부가 기능 추가

---
