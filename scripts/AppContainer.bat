@echo off
cd /d %~dp0..
docker build -t product-crud .
if /i "%ERRORLEVEL%"=="0" (
    docker run --name product-crud -p 8501:8501 -d product-crud
)