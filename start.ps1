# BOM生成系统PowerShell启动脚本

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "        BOM生成系统启动脚本" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# 检查Python环境
Write-Host "正在检查Python环境..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Python环境检查通过: $pythonVersion" -ForegroundColor Green
    } else {
        Write-Host "❌ 未找到Python环境，请先安装Python 3.7+" -ForegroundColor Red
        Read-Host "按回车键退出"
        exit 1
    }
} catch {
    Write-Host "❌ Python环境检查失败: $_" -ForegroundColor Red
    Read-Host "按回车键退出"
    exit 1
}

Write-Host ""

# 检查pip
Write-Host "正在检查pip包管理器..." -ForegroundColor Yellow
try {
    $pipVersion = pip --version 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ pip检查通过: $pipVersion" -ForegroundColor Green
    } else {
        Write-Host "❌ pip检查失败，请检查Python安装" -ForegroundColor Red
        Read-Host "按回车键退出"
        exit 1
    }
} catch {
    Write-Host "❌ pip检查失败: $_" -ForegroundColor Red
    Read-Host "按回车键退出"
    exit 1
}

Write-Host ""

# 安装依赖包
Write-Host "正在安装依赖包..." -ForegroundColor Yellow
try {
    pip install -r requirements.txt
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ 依赖包安装成功" -ForegroundColor Green
    } else {
        Write-Host "⚠️  依赖包安装可能有问题，但继续尝试启动..." -ForegroundColor Yellow
    }
} catch {
    Write-Host "⚠️  依赖包安装异常: $_" -ForegroundColor Yellow
    Write-Host "继续尝试启动..." -ForegroundColor Yellow
}

Write-Host ""

# 显示系统信息
Write-Host "系统信息:" -ForegroundColor Cyan
Write-Host "  主页面：http://localhost:5000" -ForegroundColor White
Write-Host "  管理页面：http://localhost:5000/admin" -ForegroundColor White
Write-Host ""

# 获取本机IP地址
try {
    $ipAddress = (Get-NetIPAddress -AddressFamily IPv4 | Where-Object {$_.IPAddress -like "192.168.*" -or $_.IPAddress -like "10.*" -or $_.IPAddress -like "172.*"} | Select-Object -First 1).IPAddress
    if ($ipAddress) {
        Write-Host "局域网访问地址：http://$ipAddress`:5000" -ForegroundColor Cyan
        Write-Host ""
    }
} catch {
    Write-Host "无法获取局域网IP地址" -ForegroundColor Yellow
}

Write-Host "按 Ctrl+C 停止系统" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# 启动系统
try {
    python app.py
} catch {
    Write-Host "❌ 系统启动失败: $_" -ForegroundColor Red
    Write-Host ""
    Write-Host "可能的解决方案:" -ForegroundColor Yellow
    Write-Host "1. 检查Python版本是否为3.7+" -ForegroundColor White
    Write-Host "2. 检查依赖包是否正确安装" -ForegroundColor White
    Write-Host "3. 检查端口5000是否被占用" -ForegroundColor White
    Write-Host "4. 查看错误日志获取详细信息" -ForegroundColor White
}

Write-Host ""
Read-Host "按回车键退出"
