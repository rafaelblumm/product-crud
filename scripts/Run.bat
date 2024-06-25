@echo off
rem Configura Venv se não estiver configurado no prompt corrente
if not defined VIRTUAL_ENV (
   call ConfigureVenv.bat
)
rem Inicia server do Streamlit
cd %~dp0..
set CMD=streamlit run src/run.py --server.port=8501 --server.address=localhost
echo *** Iniciando servidor (%CMD%)
%CMD%
