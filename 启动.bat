@echo off
chcp 65001 >nul
cd /d "%~dp0"

echo ========================================
echo   随机抽取器 - 启动中
echo ========================================
echo.

where python >nul 2>&1
if errorlevel 1 (
    echo [错误] 未找到 Python，请先安装 Python 3.8+ 并加入 PATH。
    echo 下载地址: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo [检测] Python 环境 OK
python --version

set DEPS=PySide6 pypinyin
set NEED_INSTALL=

for %%d in (%DEPS%) do (
    python -c "import %%d" >nul 2>&1
    if errorlevel 1 (
        echo [缺失] %%d
        set NEED_INSTALL=1
    ) else (
        echo [已装 ] %%d
    )
)

if defined NEED_INSTALL (
    echo.
    echo [安装] 正在补装缺失依赖，请稍候 ...
    python -m pip install PySide6 pypinyin
    if errorlevel 1 (
        echo.
        echo [错误] 依赖安装失败，请检查网络或手动执行:
        echo        python -m pip install PySide6 pypinyin
        pause
        exit /b 1
    )
    echo [安装] 完成
)

echo.
echo [启动] python main.py
echo ----------------------------------------

python main.py
if errorlevel 1 (
    echo.
    echo [错误] 程序异常退出，错误码: %errorlevel%
    pause
)