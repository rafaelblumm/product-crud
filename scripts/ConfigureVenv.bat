@echo off
rem Testa se Python está instalado
call python --version > nul 2>&1
if /i not "%ERRORLEVEL%"=="0" (
   echo *** ERRO: Python não está instalado corretamente
   goto :End
)
rem Altera diretório para raíz do projeto
set ORIGINAL_DIR=%CD%
cd /d %~dp0..
rem Configura script
call :InstallVenv
call :ConfigurePrompt
call :InstallDependencies
goto :End

rem Instala Venv se já não estiver instalado
:InstallVenv
if exist %CD%\venv\Scripts\activate.bat (
   goto :eof
)
set CMD=python -m venv Venv
echo *** Instalando Venv (%CMD%)
call %CMD%
goto :eof

rem Configura o prompt corrente
:ConfigurePrompt
set CMD=venv\scripts\activate.bat
echo.
echo *** Ativando Venv no prompt corrente (%CMD%)
call %CMD%
goto :eof

rem Instala dependências
:InstallDependencies
if exist %CD%\venv\Scripts\streamlit.cmd (
   goto :eof
)
set CMD=python -m pip install -r requirements.txt
echo.
echo *** Instalando dependências (%CMD%)
call %CMD%
goto :eof


rem Finaliza o script e restaura diretório anterior
:End
cd %ORIGINAL_DIR%
set ORIGINAL_DIR=
set CMD=
