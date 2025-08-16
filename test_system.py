#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BOM生成系统测试脚本
用于验证系统的基本功能是否正常
"""

import requests
import json
import time
import os
import sys

# 测试配置
BASE_URL = 'http://localhost:5000'
TEST_TIMEOUT = 10

def test_server_connection():
    """测试服务器连接"""
    print("🔍 测试服务器连接...")
    try:
        response = requests.get(f"{BASE_URL}/", timeout=TEST_TIMEOUT)
        if response.status_code == 200:
            print("✅ 服务器连接成功")
            return True
        else:
            print(f"❌ 服务器响应异常: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ 无法连接到服务器: {e}")
        return False

def test_api_endpoints():
    """测试API端点"""
    print("\n🔍 测试API端点...")
    
    # 测试获取配方列表
    try:
        response = requests.get(f"{BASE_URL}/api/recipes", timeout=TEST_TIMEOUT)
        if response.status_code == 200:
            recipes = response.json()
            print(f"✅ 获取配方列表成功，共 {len(recipes)} 个配方")
        else:
            print(f"❌ 获取配方列表失败: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 获取配方列表异常: {e}")
        return False
    
    return True

def test_recipe_management():
    """测试配方管理功能"""
    print("\n🔍 测试配方管理功能...")
    
    # 测试下载模板
    try:
        response = requests.get(f"{BASE_URL}/api/recipe/template", timeout=TEST_TIMEOUT)
        if response.status_code == 200:
            print("✅ 下载配方模板成功")
        else:
            print(f"❌ 下载配方模板失败: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 下载配方模板异常: {e}")
        return False
    
    return True

def test_bom_generation():
    """测试BOM生成功能"""
    print("\n🔍 测试BOM生成功能...")
    
    # 获取第一个配方ID
    try:
        response = requests.get(f"{BASE_URL}/api/recipes", timeout=TEST_TIMEOUT)
        if response.status_code != 200:
            print("❌ 无法获取配方列表")
            return False
        
        recipes = response.json()
        if not recipes:
            print("❌ 没有可用的配方")
            return False
        
        recipe_id = recipes[0]['id']
        print(f"✅ 使用配方ID: {recipe_id}")
        
    except Exception as e:
        print(f"❌ 获取配方失败: {e}")
        return False
    
    # 测试BOM生成
    bom_data = {
        "parent_material_code": "TEST001",
        "parent_material_name": "测试产品",
        "basic_quantity": 1.0,
        "basic_unit": "PCS",
        "recipe_id": recipe_id
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/generate_bom",
            json=bom_data,
            timeout=TEST_TIMEOUT
        )
        
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                print("✅ BOM生成成功")
                print(f"   文件路径: {result.get('file_path', 'N/A')}")
                return True
            else:
                print(f"❌ BOM生成失败: {result.get('message', '未知错误')}")
                return False
        else:
            print(f"❌ BOM生成请求失败: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ BOM生成异常: {e}")
        return False

def test_admin_page():
    """测试管理页面"""
    print("\n🔍 测试管理页面...")
    try:
        response = requests.get(f"{BASE_URL}/admin", timeout=TEST_TIMEOUT)
        if response.status_code == 200:
            print("✅ 管理页面访问成功")
            return True
        else:
            print(f"❌ 管理页面访问失败: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 管理页面访问异常: {e}")
        return False

def run_all_tests():
    """运行所有测试"""
    print("=" * 50)
    print("🚀 BOM生成系统功能测试")
    print("=" * 50)
    
    tests = [
        ("服务器连接", test_server_connection),
        ("API端点", test_api_endpoints),
        ("配方管理", test_recipe_management),
        ("BOM生成", test_bom_generation),
        ("管理页面", test_admin_page)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
            else:
                print(f"⚠️  {test_name} 测试失败")
        except Exception as e:
            print(f"❌ {test_name} 测试异常: {e}")
    
    print("\n" + "=" * 50)
    print(f"📊 测试结果: {passed}/{total} 通过")
    
    if passed == total:
        print("🎉 所有测试通过！系统运行正常")
        return True
    else:
        print("⚠️  部分测试失败，请检查系统配置")
        return False

def check_system_status():
    """检查系统状态"""
    print("\n🔍 检查系统状态...")
    
    # 检查数据库文件
    db_files = ['bom_system.db', 'bom_system_dev.db']
    for db_file in db_files:
        if os.path.exists(db_file):
            size = os.path.getsize(db_file)
            print(f"✅ 数据库文件 {db_file} 存在 ({size} bytes)")
        else:
            print(f"❌ 数据库文件 {db_file} 不存在")
    
    # 检查模板文件
    template_dir = 'templates'
    if os.path.exists(template_dir):
        files = os.listdir(template_dir)
        print(f"✅ 模板目录存在，包含 {len(files)} 个文件")
        for file in files:
            print(f"   - {file}")
    else:
        print("❌ 模板目录不存在")
    
    # 检查Python文件
    python_files = ['app.py', 'config.py']
    for py_file in python_files:
        if os.path.exists(py_file):
            print(f"✅ Python文件 {py_file} 存在")
        else:
            print(f"❌ Python文件 {py_file} 不存在")

def main():
    """主函数"""
    if len(sys.argv) > 1 and sys.argv[1] == '--status':
        check_system_status()
        return
    
    print("正在启动测试...")
    print("请确保BOM生成系统正在运行 (python app.py)")
    print(f"系统地址: {BASE_URL}")
    print()
    
    # 等待用户确认
    input("按回车键开始测试...")
    
    # 运行测试
    success = run_all_tests()
    
    if success:
        print("\n🎯 系统测试完成，可以正常使用！")
        print(f"访问地址: {BASE_URL}")
        print(f"管理地址: {BASE_URL}/admin")
    else:
        print("\n⚠️  系统存在问题，请检查配置和日志")
    
    print("\n按回车键退出...")
    input()

if __name__ == '__main__':
    main()
