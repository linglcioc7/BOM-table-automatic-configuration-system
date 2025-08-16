@echo off
chcp 65001 >nul
title BOM生成系统 - 防火墙配置

echo ========================================
echo    BOM生成系统 - 防火墙配置
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

echo 🔍 正在配置Windows防火墙...
echo.

:: 添加入站规则 - TCP 5000端口
echo 📡 添加TCP入站规则...
netsh advfirewall firewall add rule name="BOM生成系统-TCP" dir=in action=allow protocol=TCP localport=5000 profile=any description="BOM生成系统TCP端口访问"

:: 添加入站规则 - UDP 5000端口（如果需要）
echo 📡 添加UDP入站规则...
netsh advfirewall firewall add rule name="BOM生成系统-UDP" dir=in action=allow protocol=UDP localport=5000 profile=any description="BOM生成系统UDP端口访问"

:: 添加出站规则
echo 📡 添加出站规则...
netsh advfirewall firewall add rule name="BOM生成系统-Out" dir=out action=allow protocol=TCP localport=5000 profile=any description="BOM生成系统出站访问"

echo.
echo ✅ 防火墙配置完成！
echo.
echo 📋 已添加的规则：
echo     - BOM生成系统-TCP (入站)
echo     - BOM生成系统-UDP (入站)
echo     - BOM生成系统-Out (出站)
echo.
echo 🌐 现在局域网内的其他计算机可以访问：
echo     http://[本机IP]:5000
echo.
echo ⚠️  提示：如果仍有访问问题，请检查：
echo     1. 本机IP地址是否正确
echo     2. 其他计算机是否在同一网段
echo     3. 路由器设置是否允许内网通信
echo.

pause
