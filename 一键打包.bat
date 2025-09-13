@echo off
chcp 65001 >nul
title BOM生成系统 - 一键打包

echo ========================================
echo    BOM生成系统 - 一键打包脚本
echo ========================================
echo.

echo 🔍 检查环境...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 错误：未找到Python
    pause
    exit /b 1
)

pip show pyinstaller >nul 2>&1
if errorlevel 1 (
    echo ❌ 错误：未安装PyInstaller
    echo 正在安装...
    pip install pyinstaller
    if errorlevel 1 (
        echo ❌ 安装失败
        pause
        exit /b 1
    )
)

echo ✅ 环境检查通过
echo.

echo 🚀 开始一键打包...
echo.

:: 清理之前的构建文件
if exist "build" (
    echo 🧹 清理构建目录...
    rmdir /s /q build
)

if exist "dist" (
    echo 🧹 清理输出目录...
    rmdir /s /q dist
)

:: 打包控制台版本
echo 📦 步骤1: 打包控制台版本...
pyinstaller --clean bom_system.spec
if errorlevel 1 (
    echo ❌ 控制台版本打包失败
    pause
    exit /b 1
)
echo ✅ 控制台版本打包完成

:: 打包GUI版本
echo.
echo 📦 步骤2: 打包GUI版本...
pyinstaller --clean bom_system_gui.spec
if errorlevel 1 (
    echo ❌ GUI版本打包失败
    pause
    exit /b 1
)
echo ✅ GUI版本打包完成

echo.
echo ========================================
echo    🎉 一键打包完成！
echo ========================================
echo.
echo 📁 输出文件位置：dist\
echo.
echo 📊 生成的文件：
echo     - BOM生成系统.exe (控制台版本)
echo     - BOM生成系统-无控制台.exe (GUI版本)
echo.

echo 📋 文件说明：
echo     🔧 控制台版本：适合开发者和管理员，显示运行日志
echo     🎨 GUI版本：适合普通用户，无控制台窗口，更美观
echo.

echo 🎯 使用建议：
echo     - 分发给普通用户：使用GUI版本
echo     - 系统管理员使用：使用控制台版本
echo     - 两个版本功能完全相同
echo.

echo 🎉 打包成功！按任意键退出...
pause >nul
