# BOM生成系统配置文件

import os

class Config:
    """基础配置类"""
    
    # 基本设置
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'bom-system-secret-key-2024'
    DEBUG = False
    TESTING = False
    
    # 数据库设置
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///bom_system.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # 文件上传设置
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
    UPLOAD_FOLDER = 'uploads'
    
    # 系统设置
    DEFAULT_FACTORY_CODE = 'P060'  # 默认工厂代码
    DEFAULT_BOM_PURPOSE = '1'      # 默认BOM用途
    DEFAULT_BOM_STATUS = '01'      # 默认BOM状态
    DEFAULT_PROJECT_CATEGORY = 'L' # 默认项目类别
    
    # 行项目号设置
    LINE_NUMBER_START = '0010'     # 行项目号起始值
    LINE_NUMBER_STEP = 10          # 行项目号步长
    LINE_NUMBER_FORMAT = '4'       # 行项目号格式（4位数字）
    
    # 数量精度设置
    MAX_DECIMAL_PLACES = 3         # 最大小数位数
    
    # 分页设置
    ITEMS_PER_PAGE = 20
    
    # 日志设置
    LOG_LEVEL = 'INFO'
    LOG_FILE = 'bom_system.log'
    
    # 安全设置
    SESSION_COOKIE_SECURE = False
    SESSION_COOKIE_HTTPONLY = True
    PERMANENT_SESSION_LIFETIME = 3600  # 1小时

class DevelopmentConfig(Config):
    """开发环境配置"""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///bom_system_dev.db'

class ProductionConfig(Config):
    """生产环境配置"""
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    
    # 生产环境安全设置
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True

class TestingConfig(Config):
    """测试环境配置"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///bom_system_test.db'

# 配置字典
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}

# 项目类别选项
PROJECT_CATEGORIES = [
    'L',  # 固定值
    'N'   # 虚拟件
]

# BOM用途选项
BOM_PURPOSES = [
    '1',  # 生产
    '2',  # 销售
    '3',  # 工程
    '4',  # 成本核算
    '5'   # 其他
]

# BOM状态选项
BOM_STATUSES = [
    '01',  # 有效
    '02',  # 无效
    '03',  # 待审核
    '04'   # 已废弃
]

# Excel导出设置
EXCEL_SETTINGS = {
    'sheet_name': 'BOM表',
    'column_widths': [15, 10, 20, 20, 30, 15, 10, 10, 10, 15, 15, 15, 20, 30, 15, 15],
    'header_style': {
        'font': {'bold': True, 'size': 12},
        'alignment': {'horizontal': 'center', 'vertical': 'center'},
        'fill': {'fgColor': 'CCCCCC'}
    },
    'data_style': {
        'font': {'size': 10},
        'alignment': {'horizontal': 'left', 'vertical': 'center'}
    }
}

# 系统信息
SYSTEM_INFO = {
    'name': 'BOM生成系统',
    'version': '1.0.0',
    'description': '自动生成物料清单表的Web应用系统',
    'author': 'System Administrator',
    'contact': 'admin@company.com'
}
