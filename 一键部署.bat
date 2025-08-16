@echo off
chcp 65001 >nul
title BOM生成系统 - 一键部署

echo ========================================
echo    BOM生成系统 - 一键部署脚本
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

echo 🚀 开始一键部署BOM生成系统...
echo.

:: 步骤1: 检查Python环境
echo 📋 步骤1: 检查Python环境...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 错误：未找到Python，请先安装Python 3.8+
    echo 下载地址：https://www.python.org/downloads/
    pause
    exit /b 1
)
echo ✅ Python环境检查通过

:: 步骤2: 安装依赖包
echo.
echo 📋 步骤2: 安装依赖包...
echo 🔍 检查Flask是否已安装...
pip show flask >nul 2>&1
if errorlevel 1 (
    echo 📦 正在安装依赖包...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ❌ 依赖安装失败，请检查网络连接
        pause
        exit /b 1
    )
    echo ✅ 依赖包安装完成
) else (
    echo ✅ 依赖包已安装
)

:: 步骤3: 配置防火墙
echo.
echo 📋 步骤3: 配置防火墙...
echo 🔒 正在配置Windows防火墙...
netsh advfirewall firewall add rule name="BOM生成系统-TCP" dir=in action=allow protocol=TCP localport=5000 profile=any description="BOM生成系统TCP端口访问" >nul 2>&1
netsh advfirewall firewall add rule name="BOM生成系统-UDP" dir=in action=allow protocol=UDP localport=5000 profile=any description="BOM生成系统UDP端口访问" >nul 2>&1
netsh advfirewall firewall add rule name="BOM生成系统-Out" dir=out action=allow protocol=TCP localport=5000 profile=any description="BOM生成系统出站访问" >nul 2>&1
echo ✅ 防火墙配置完成

:: 步骤4: 检查端口占用
echo.
echo 📋 步骤4: 检查端口占用...
netstat -an | findstr ":5000" >nul
if not errorlevel 1 (
    echo ⚠️  警告：端口5000已被占用
    echo 正在尝试关闭占用进程...
    for /f "tokens=5" %%a in ('netstat -ano ^| findstr ":5000"') do (
        taskkill /f /pid %%a >nul 2>&1
    )
    echo ✅ 端口5000已释放
) else (
    echo ✅ 端口5000可用
)

:: 步骤5: 启动系统
echo.
echo 📋 步骤5: 启动系统...
echo 🚀 正在启动BOM生成系统...

:: 后台启动应用
start /min python app.py

:: 等待系统启动
echo ⏳ 等待系统启动...
timeout /t 10 /nobreak >nul

:: 检查系统是否启动成功
echo 🔍 检查系统状态...
netstat -an | findstr ":5000" >nul
if errorlevel 1 (
    echo ❌ 系统启动失败，请检查错误信息
    pause
    exit /b 1
)

:: 获取本机IP地址
echo.
echo 📍 获取本机IP地址...
for /f "tokens=2 delims=:" %%i in ('ipconfig ^| findstr "IPv4"') do (
    set "IP=%%i"
    set "IP=!IP: =!"
    goto :found_ip
)
:found_ip

echo.
echo ========================================
echo    🎉 部署完成！
echo ========================================
echo.
echo ✅ 系统已成功启动
echo.
echo 🌐 访问地址：
echo     本机访问：http://localhost:5000
echo     局域网访问：http://!IP!:5000
echo.
echo 👥 管理员账户：
echo     用户名：shwx
echo     密码：shwxjsb
echo.
echo 📋 下一步操作：
echo     1. 在浏览器中访问上述地址
echo     2. 使用管理员账户登录配方管理系统
echo     3. 导入或创建配方数据
echo     4. 测试BOM生成功能
echo.
echo 🛠️  管理命令：
echo     查看网络状态：check_network.bat
echo     启动生产环境：start_production.bat
echo     安装系统服务：install_service.bat
echo.
echo 📚 详细说明请查看：局域网部署说明.md
echo.

pause
