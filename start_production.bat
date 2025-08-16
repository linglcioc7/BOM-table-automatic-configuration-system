@echo off
chcp 65001 >nul
title BOM生成系统 - 生产环境

echo ========================================
echo    BOM生成系统 - 生产环境启动脚本
echo ========================================
echo.

:: 检查Python是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 错误：未找到Python，请先安装Python 3.8+
    pause
    exit /b 1
)

:: 检查依赖是否安装
echo 🔍 检查依赖包...
pip show flask >nul 2>&1
if errorlevel 1 (
    echo ❌ 错误：未安装Flask，正在安装依赖包...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ❌ 依赖安装失败，请检查网络连接
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

:: 启动应用
echo ✅ 环境检查完成，正在启动BOM生成系统...
echo.
echo 📍 访问地址：
echo    本机访问：http://localhost:5000
echo    局域网访问：http://[本机IP]:5000
echo.
echo ⚠️  提示：按 Ctrl+C 停止服务
echo.

:: 启动应用
python app.py

:: 如果应用异常退出，显示错误信息
if errorlevel 1 (
    echo.
    echo ❌ 应用异常退出，错误代码：%errorlevel%
    echo 请检查日志信息或联系管理员
    pause
)
