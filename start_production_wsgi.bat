@echo off
chcp 65001 >nul
title BOM生成系统 - 生产环境WSGI启动

echo ========================================
echo    BOM生成系统 - 生产环境WSGI启动
echo ========================================
echo.

:: 检查Python是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 错误：未找到Python，请先安装Python 3.8+
    pause
    exit /b 1
)

:: 检查waitress是否安装
pip show waitress >nul 2>&1
if errorlevel 1 (
    echo 📦 正在安装生产级WSGI服务器...
    pip install waitress
    if errorlevel 1 (
        echo ❌ 安装失败，请检查网络连接
        pause
        exit /b 1
    )
)

:: 检查端口是否被占用
echo 🔍 检查端口5000是否可用...
netstat -an | findstr ":5000" >nul
if not errorlevel 1 (
    echo ❌ 错误：端口5000已被占用，请关闭其他应用
    echo 占用端口的进程：
    netstat -ano | findstr ":5000"
    pause
    exit /b 1
)

:: 启动生产级WSGI服务器
echo ✅ 环境检查完成，正在启动生产级WSGI服务器...
echo.
echo 📍 访问地址：
echo    本机访问：http://localhost:5000
echo    局域网访问：http://[本机IP]:5000
echo.
echo 🚀 使用Waitress WSGI服务器，适合生产环境
echo ⚠️  提示：按 Ctrl+C 停止服务
echo.

:: 启动Waitress服务器
python -m waitress --host=0.0.0.0 --port=5000 app:app

:: 如果应用异常退出，显示错误信息
if errorlevel 1 (
    echo.
    echo ❌ 应用异常退出，错误代码：%errorlevel%
    echo 请检查日志信息或联系管理员
    pause
)
