#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BOM生成系统演示脚本
展示系统的主要功能和特性
"""

import os
import sys
import time

def print_banner():
    """打印系统横幅"""
    print("=" * 60)
    print("🚀 BOM生成系统 - 功能演示")
    print("=" * 60)
    print()

def print_feature(title, description, code=None):
    """打印功能特性"""
    print(f"📋 {title}")
    print(f"   {description}")
    if code:
        print(f"   代码示例: {code}")
    print()

def print_system_info():
    """打印系统信息"""
    print("🏗️  系统架构")
    print("   • 后端: Python Flask + SQLAlchemy + SQLite")
    print("   • 前端: HTML + JavaScript + Bootstrap 5")
    print("   • 数据库: SQLite (轻量级，无需额外安装)")
    print("   • 文件格式: Excel (.xlsx)")
    print()

def print_main_features():
    """打印主要功能"""
    print("✨ 主要功能")
    
    print_feature(
        "BOM表自动生成",
        "根据配方自动生成标准格式的BOM表，支持17列字段",
        "POST /api/generate_bom"
    )
    
    print_feature(
        "配方管理",
        "完整的配方CRUD操作，支持增删改查、导入导出",
        "GET/POST/PUT/DELETE /api/recipe"
    )
    
    print_feature(
        "Excel导入导出",
        "支持配方模板下载、配方导入、配方导出功能",
        "/api/recipe/template, /api/recipe/import, /api/recipe/export"
    )
    
    print_feature(
        "Web界面",
        "基于浏览器的友好用户界面，支持局域网访问",
        "http://localhost:5000"
    )

def print_recipe_management():
    """打印配方管理功能"""
    print("🔧 配方管理功能")
    
    print_feature(
        "配方添加",
        "通过Web界面添加新配方，支持动态添加配方项",
        "showAddRecipeModal()"
    )
    
    print_feature(
        "配方编辑",
        "修改现有配方的名称、描述和配方项",
        "showEditRecipeModal(recipeId)"
    )
    
    print_feature(
        "配方删除",
        "软删除配方（设置is_active为False）",
        "DELETE /api/recipe/{id}"
    )
    
    print_feature(
        "配方查看",
        "查看配方的详细信息和配方项列表",
        "viewRecipe(recipeId)"
    )
    
    print_feature(
        "配方导入",
        "从Excel文件批量导入配方数据",
        "POST /api/recipe/import"
    )
    
    print_feature(
        "配方导出",
        "将配方导出为Excel格式文件",
        "GET /api/recipe/export/{id}"
    )
    
    print_feature(
        "模板下载",
        "下载标准配方导入模板",
        "GET /api/recipe/template"
    )

def print_bom_structure():
    """打印BOM表结构"""
    print("📊 BOM表字段结构 (17列)")
    print("   A: 字段名称     B: 工厂        C: BOM可选文本")
    print("   D: 父项物料号   E: 物料名称    F: 生效日期")
    print("   G: BOM用途     H: 可选BOM     I: BOM状态")
    print("   J: 基本数量     K: 基本单位    L: 行项目号")
    print("   M: 项目类别     N: 子项物料号  O: 子项物料描述")
    print("   P: 子项数量     Q: 子项单位")
    print()

def print_usage_flow():
    """打印使用流程"""
    print("🔄 使用流程")
    print("   1. 系统初始化 → 自动创建示例数据和数据库")
    print("   2. 配方管理 → 添加/编辑/删除配方，支持导入导出")
    print("   3. 生成BOM → 填写信息，选择配方，生成Excel")
    print("   4. 下载使用 → 系统自动生成并下载BOM表")
    print()

def print_deployment_info():
    """打印部署信息"""
    print("🌐 部署方式")
    print("   • 本地运行: python app.py")
    print("   • 局域网部署: 修改host为0.0.0.0")
    print("   • 生产环境: 使用Gunicorn + Nginx")
    print("   • 访问地址: http://[IP]:5000")
    print()

def print_quick_start():
    """打印快速开始"""
    print("🚀 快速开始")
    print("   1. 安装依赖: pip install -r requirements.txt")
    print("   2. 启动系统: python app.py")
    print("   3. 访问系统: http://localhost:5000")
    print("   4. 管理配方: http://localhost:5000/admin")
    print()

def print_file_structure():
    """打印文件结构"""
    print("📁 项目文件结构")
    files = [
        ("app.py", "主应用文件，包含Flask应用和完整API"),
        ("config.py", "配置文件，管理系统设置"),
        ("requirements.txt", "Python依赖包列表"),
        ("templates/", "HTML模板目录"),
        ("templates/index.html", "主页面模板"),
        ("templates/admin.html", "管理页面模板（支持CRUD）"),
        ("start.bat", "Windows批处理启动脚本"),
        ("start.ps1", "PowerShell启动脚本"),
        ("test_system.py", "系统功能测试脚本"),
        ("README.md", "详细使用说明文档")
    ]
    
    for filename, description in files:
        print(f"   • {filename:<20} - {description}")
    print()

def print_advantages():
    """打印系统优势"""
    advantages = [
        "自动化程度高，减少手工操作错误",
        "配方管理完整，支持增删改查、导入导出",
        "行号格式标准，支持0010、0020等格式",
        "Excel导入导出，便于批量操作",
        "Web界面友好，支持多用户访问",
        "部署简单，无需复杂环境配置",
        "开源技术栈，易于二次开发"
    ]
    
    for advantage in advantages:
        print(f"   ✓ {advantage}")
    print()

def print_contact():
    """打印联系信息"""
    print("📞 技术支持")
    print("   • 系统版本: 1.0.0")
    print("   • 开发语言: Python 3.7+")
    print("   • 框架版本: Flask 2.3.3")
    print("   • 更新日期: 2024年8月")
    print()

def main():
    """主函数"""
    print_banner()
    
    print_system_info()
    print_main_features()
    print_recipe_management()
    print_bom_structure()
    print_usage_flow()
    print_deployment_info()
    print_quick_start()
    print_file_structure()
    print_advantages()
    print_contact()
    
    print("=" * 60)
    print("🎯 演示完成！系统已准备就绪")
    print("   运行 'python app.py' 启动系统")
    print("=" * 60)

if __name__ == '__main__':
    main()
