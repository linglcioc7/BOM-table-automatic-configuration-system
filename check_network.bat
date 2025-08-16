@echo off
chcp 65001 >nul
title BOM生成系统 - 网络配置检查

echo ========================================
echo    BOM生成系统 - 网络配置检查
echo ========================================
echo.

echo 🔍 正在检查网络配置...
echo.

:: 显示本机IP地址
echo 📍 本机IP地址：
ipconfig | findstr "IPv4"
echo.

:: 显示网络适配器信息
echo 📡 网络适配器状态：
ipconfig /all | findstr "适配器"
echo.

:: 检查端口5000是否被占用
echo 🔍 检查端口5000状态：
netstat -an | findstr ":5000"
if errorlevel 1 (
    echo ✅ 端口5000未被占用
) else (
    echo ⚠️  端口5000已被占用
)
echo.

:: 检查防火墙状态
echo 🔒 检查Windows防火墙状态：
netsh advfirewall show allprofiles state | findstr "状态"
echo.

:: 检查BOM生成系统防火墙规则
echo 🔍 检查BOM生成系统防火墙规则：
netsh advfirewall firewall show rule name="BOM生成系统*" | findstr "规则名称"
echo.

:: 测试本地连接
echo 🔍 测试本地连接：
ping -n 1 127.0.0.1 >nul
if errorlevel 1 (
    echo ❌ 本地连接失败
) else (
    echo ✅ 本地连接正常
)
echo.

:: 显示访问地址
echo 🌐 访问地址：
echo     本机访问：http://localhost:5000
echo     本机IP访问：http://127.0.0.1:5000
echo.
echo 📋 局域网访问地址（请将[本机IP]替换为实际IP）：
for /f "tokens=2 delims=:" %%i in ('ipconfig ^| findstr "IPv4"') do (
    set "IP=%%i"
    set "IP=!IP: =!"
    echo     http://!IP!:5000
)
echo.

:: 显示网络诊断命令
echo 🛠️  网络诊断命令：
echo     测试端口：telnet [目标IP] 5000
echo     测试连接：ping [目标IP]
echo     查看路由：tracert [目标IP]
echo.

pause
