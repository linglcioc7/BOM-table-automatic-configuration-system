@echo off
chcp 65001 >nul
title BOM生成系统 - 服务安装

echo ========================================
echo    BOM生成系统 - Windows服务安装
echo ========================================
echo.

:: 检查管理员权限
net session >nul 2>&1
if errorlevel 1 (
    echo ❌ 错误：需要管理员权限运行此脚本
    echo 请右键点击此文件，选择"以管理员身份运行"
    pause
    exit /b 1
)

:: 检查nssm是否可用
nssm --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 错误：未找到nssm工具"
    echo 请先下载nssm并添加到系统PATH中"
    echo 下载地址：https://nssm.cc/download"
    pause
    exit /b 1
)

:: 获取当前目录
set "CURRENT_DIR=%~dp0"
set "PYTHON_PATH=python.exe"
set "SCRIPT_PATH=%CURRENT_DIR%app.py"

:: 检查文件是否存在
if not exist "%SCRIPT_PATH%" (
    echo ❌ 错误：未找到app.py文件"
    echo 当前目录：%CURRENT_DIR%"
    pause
    exit /b 1
)

echo 🔍 正在安装BOM生成系统服务...
echo 服务名称：BOM生成系统
echo 程序路径：%PYTHON_PATH%
echo 脚本路径：%SCRIPT_PATH%
echo.

:: 安装服务
nssm install "BOM生成系统" "%PYTHON_PATH%" "%SCRIPT_PATH%"
if errorlevel 1 (
    echo ❌ 服务安装失败"
    pause
    exit /b 1
)

:: 设置服务描述
nssm set "BOM生成系统" Description "BOM表格自动配置系统 - 配方管理和BOM生成"

:: 设置启动类型为自动
nssm set "BOM生成系统" Start SERVICE_AUTO_START

:: 设置工作目录
nssm set "BOM生成系统" AppDirectory "%CURRENT_DIR%"

:: 设置环境变量
nssm set "BOM生成系统" AppEnvironmentExtra "FLASK_ENV=production"

:: 启动服务
echo 🔍 正在启动服务...
nssm start "BOM生成系统"
if errorlevel 1 (
    echo ❌ 服务启动失败"
    echo 请检查服务配置或手动启动"
    pause
    exit /b 1
)

echo.
echo ✅ 服务安装成功！
echo.
echo 📋 服务信息：
echo     服务名称：BOM生成系统
echo     启动类型：自动启动
echo     状态：正在运行
echo.
echo 🛠️  管理命令：
echo     启动服务：nssm start "BOM生成系统"
echo     停止服务：nssm stop "BOM生成系统"
echo     重启服务：nssm restart "BOM生成系统"
echo     删除服务：nssm remove "BOM生成系统" confirm
echo.
echo 🌐 访问地址：http://localhost:5000
echo.

pause
