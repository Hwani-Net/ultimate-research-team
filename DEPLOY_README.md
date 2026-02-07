# 🚀 Ultimate Research Team - 배포 가이드 (Cloudflare & GitHub)

본 프로젝트를 Cloudflare Pages와 GitHub을 통해 배포하는 프로토콜입니다.

## 1. GitHub 연동
1. **GitHub 리포지토리 생성**: 새로운 리포지토리를 생성합니다.
2. **코드 푸시**:
   ```bash
   git remote add origin [YOUR_GITHUB_REPO_URL]
   git push -u origin master
   ```

## 2. GitHub Secrets 설정
GitHub 리포지토리의 `Settings > Secrets and variables > Actions`에서 아래 항목을 추가합니다.
- `CLOUDFLARE_API_TOKEN`: Cloudflare에서 발급받은 API 토큰.
- `CLOUDFLARE_ACCOUNT_ID`: Cloudflare 계정 ID.

## 3. Cloudflare Pages 설정
이 앱은 Python/Streamlit 기반이므로, Cloudflare Pages에서 구동하기 위해 두 가지 방법이 있습니다.

### 방법 A: Stlite (브라우저 직접 구동)
- `index_stlite.html`을 사용하여 서버 없이 브라우저에서 Pyodide로 구동합니다.
- 파일 및 API 호출(CORS) 관련 제약이 있을 수 있습니다.

### 방법 B: Streamlit Cloud (권장)
- 가장 안정적인 배포 방식입니다.
- GitHub 리포지토리를 [Streamlit Cloud](https://share.streamlit.io/)에 연결하기만 하면 즉시 배포됩니다.
- Cloudflare를 앞단(Proxy)에 두어 보안과 이 커스텀 도메인을 적용할 수 있습니다.

## 4. 환경 변수 (Secrets) 관리
배포 환경(Cloudflare Dashboard 또는 Streamlit Cloud)의 설정 메뉴에서 아래 변수를 등록하십시오.
- `GEMINI_API_KEY`: Google Gemini API 키

---
**Status**: `Deployment Files Prepared`
**Manual Link**: `ANTIGRAVITY_MASTER_MANUAL.md` 배포 프로토콜 참조
