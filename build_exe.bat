@echo off
chcp 65001 >nul
title BOM生成系统 - EXE打包

echo ========================================
echo    BOM生成系统 - EXE打包脚本
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

echo 🚀 开始打包...
echo 📦 使用配置文件：bom_system.spec
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

:: 开始打包
echo 📦 正在打包，请稍候...
pyinstaller --clean bom_system.spec

if errorlevel 1 (
    echo ❌ 打包失败
    pause
    exit /b 1
)

echo.
echo ✅ 打包完成！
echo.
echo 📁 输出文件位置：dist\BOM生成系统.exe
echo 📊 文件大小：
dir "dist\BOM生成系统.exe" | findstr "BOM生成系统.exe"
echo.

echo 📋 下一步操作：
echo     1. 测试exe文件是否正常运行
echo     2. 将exe文件分发给用户
echo     3. 用户无需安装Python即可运行
echo.

echo 🎉 打包成功！按任意键退出...
pause >nul
