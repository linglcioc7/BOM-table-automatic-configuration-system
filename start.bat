@echo off
echo ========================================
echo        BOM生成系统启动脚本
echo ========================================
echo.

echo 正在检查Python环境...
python --version >nul 2>&1
if errorlevel 1 (
    echo 错误：未找到Python环境，请先安装Python 3.7+
    pause
    exit /b 1
)

echo Python环境检查通过
echo.

echo 正在安装依赖包...
pip install -r requirements.txt
if errorlevel 1 (
    echo 警告：依赖安装可能有问题，但继续尝试启动...
    echo.
)

echo 正在启动BOM生成系统...
echo.
echo 系统将在以下地址启动：
echo 主页面：http://localhost:5000
echo 管理页面：http://localhost:5000/admin
echo.
echo 局域网访问：http://[本机IP]:5000
echo.
echo 按 Ctrl+C 停止系统
echo ========================================
echo.

python app.py

pause
