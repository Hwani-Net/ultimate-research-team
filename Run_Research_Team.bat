@echo off
title Ultimate Research Team v11.1 - Soulless Mode (5-Agent)
echo [1/3] AI 에이전트 팀을 소집하고 있습니다...
cd /d "%~dp0"

echo [2/3] 인터넷 연결 및 환경 설정을 확인 중입니다...
:: Check if streamlit is installed, if not, try to install it briefly
python -m pip install streamlit -q

echo [3/3] 브라우저를 열고 연구실 문을 엽니다!
echo.
echo ======================================================
echo   팀이 준비되었습니다. 브라우저가 열릴 때까지 기다려주세요.
echo   연구를 마치려면 이 창을 닫거나 Ctrl+C를 누르세요.
echo ======================================================
echo.

python -m streamlit run app.py

pause
