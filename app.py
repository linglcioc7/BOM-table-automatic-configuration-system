from flask import Flask, render_template, request, jsonify, send_file
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import openpyxl
from openpyxl.styles import Font, Alignment, Border, Side
import os
import tempfile
import uuid

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bom_system.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# 数据模型
class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    recipe_name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class RecipeItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'), nullable=False)
    material_code = db.Column(db.String(50), nullable=False)
    material_name = db.Column(db.String(200), nullable=False)
    quantity = db.Column(db.Float, nullable=False)
    unit = db.Column(db.String(20), nullable=False)
    line_number = db.Column(db.String(10), nullable=False)  # 改为字符串格式
    project_category = db.Column(db.String(10), default='L')

class BOMRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    parent_material_code = db.Column(db.String(50), nullable=False)
    parent_material_name = db.Column(db.String(200), nullable=False)
    basic_quantity = db.Column(db.Float, nullable=False)
    basic_unit = db.Column(db.String(20), nullable=False)
    recipe_ids = db.Column(db.Text, nullable=False)  # 存储多个配方ID，用逗号分隔
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/recipes')
def get_recipes():
    recipes = Recipe.query.filter_by(is_active=True).all()
    return jsonify([{
        'id': r.id,
        'name': r.recipe_name,
        'description': r.description,
        'created_at': r.created_at.strftime('%Y-%m-%d %H:%M:%S') if r.created_at else '',
        'updated_at': r.updated_at.strftime('%Y-%m-%d %H:%M:%S') if r.updated_at else ''
    } for r in recipes])

@app.route('/api/recipe/<int:recipe_id>')
def get_recipe_items(recipe_id):
    items = RecipeItem.query.filter_by(recipe_id=recipe_id).order_by(RecipeItem.line_number).all()
    return jsonify([{
        'id': item.id,
        'material_code': item.material_code,
        'material_name': item.material_name,
        'quantity': item.quantity,
        'unit': item.unit,
        'line_number': item.line_number,
        'project_category': item.project_category
    } for item in items])

@app.route('/api/recipe/<int:recipe_id>', methods=['PUT'])
def update_recipe(recipe_id):
    data = request.json
    recipe = Recipe.query.get(recipe_id)
    if not recipe:
        return jsonify({'success': False, 'message': '配方不存在'}), 404
    
    recipe.recipe_name = data['name']
    recipe.description = data['description']
    recipe.updated_at = datetime.utcnow()
    
    # 删除旧的配方项
    RecipeItem.query.filter_by(recipe_id=recipe_id).delete()
    
    # 添加新的配方项
    for item in data['items']:
        recipe_item = RecipeItem(
            recipe_id=recipe.id,
            material_code=item['material_code'],
            material_name=item['material_name'],
            quantity=item['quantity'],
            unit=item['unit'],
            line_number=item['line_number'],
            project_category=item['project_category']
        )
        db.session.add(recipe_item)
    
    db.session.commit()
    return jsonify({'success': True, 'message': '配方更新成功'})

@app.route('/api/recipe/<int:recipe_id>', methods=['DELETE'])
def delete_recipe(recipe_id):
    recipe = Recipe.query.get(recipe_id)
    if not recipe:
        return jsonify({'success': False, 'message': '配方不存在'}), 404
    
    # 软删除：设置is_active为False
    recipe.is_active = False
    db.session.commit()
    
    return jsonify({'success': True, 'message': '配方删除成功'})

@app.route('/api/generate_bom', methods=['POST'])
def generate_bom():
    data = request.json
    
    # 检查必要字段
    if not all(key in data for key in ['parent_material_code', 'parent_material_name', 'basic_quantity', 'basic_unit', 'recipe_ids']):
        return jsonify({'success': False, 'message': '缺少必要字段'}), 400
    
    if not data['recipe_ids']:
        return jsonify({'success': False, 'message': '请选择至少一个配方'}), 400
    
    # 创建BOM请求记录
    bom_request = BOMRequest(
        parent_material_code=data['parent_material_code'],
        parent_material_name=data['parent_material_name'],
        basic_quantity=data['basic_quantity'],
        basic_unit=data['basic_unit'],
        recipe_ids=','.join(map(str, data['recipe_ids']))  # 将配方ID数组转换为逗号分隔的字符串
    )
    db.session.add(bom_request)
    db.session.commit()
    
    # 获取所有选中的配方信息
    all_items = []
    for recipe_id in data['recipe_ids']:
        recipe = Recipe.query.get(recipe_id)
        if recipe:
            items = RecipeItem.query.filter_by(recipe_id=recipe_id).order_by(RecipeItem.line_number).all()
            # 为每个配方项添加配方信息
            for item in items:
                all_items.append({
                    'recipe_name': recipe.recipe_name,
                    'recipe_description': recipe.description,
                    'line_number': item.line_number,
                    'material_code': item.material_code,
                    'material_name': item.material_name,
                    'quantity': item.quantity,
                    'unit': item.unit,
                    'project_category': item.project_category
                })
    
    # 生成Excel文件
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "BOM表"
    
    # 设置列宽
    column_widths = [15, 10, 20, 20, 30, 15, 10, 10, 10, 15, 15, 15, 20, 30, 15, 15]
    for i, width in enumerate(column_widths, 1):
        ws.column_dimensions[openpyxl.utils.get_column_letter(i)].width = width
    
    # 表头
    headers = ['字段名称', '工厂', 'BOM可选文本', '父项物料号', '物料名称', '生效日期', 
               'BOM用途', '可选BOM', 'BOM状态', '基本数量', '基本单位', '行项目号', 
               '项目类别', '子项物料号', '子项物料描述', '子项数量', '子项单位']
    
    for col, header in enumerate(headers, 1):
        cell = ws.cell(row=1, column=col, value=header)
        cell.font = Font(bold=True)
        cell.alignment = Alignment(horizontal='center', vertical='center')
    
    # 按配方名称排序
    all_items.sort(key=lambda x: x['recipe_name'])
    
    # 数据行
    row = 2
    current_recipe = None
    bom_counter = 0
    
    for item in all_items:
        # 如果是新配方，更新计数器
        if current_recipe != item['recipe_name']:
            current_recipe = item['recipe_name']
            bom_counter += 1
        
        # 每行都填写完整的数据
        ws.cell(row=row, column=1, value='')  # 字段名称
        ws.cell(row=row, column=2, value='P060')  # 工厂
        ws.cell(row=row, column=3, value=item['recipe_description'])  # BOM可选文本
        ws.cell(row=row, column=4, value=data['parent_material_code'])  # 父项物料号
        ws.cell(row=row, column=5, value=data['parent_material_name'])  # 物料名称
        ws.cell(row=row, column=6, value='')  # 生效日期
        ws.cell(row=row, column=7, value='1')  # BOM用途
        ws.cell(row=row, column=8, value=f"{bom_counter:02d}")  # 可选BOM
        ws.cell(row=row, column=9, value='01')  # BOM状态
        ws.cell(row=row, column=10, value=data['basic_quantity'])  # 基本数量
        ws.cell(row=row, column=11, value=data['basic_unit'])  # 基本单位
        ws.cell(row=row, column=12, value=item['line_number'])  # 行项目号
        ws.cell(row=row, column=13, value=item['project_category'])  # 项目类别
        ws.cell(row=row, column=14, value=item['material_code'])  # 子项物料号
        ws.cell(row=row, column=15, value=item['material_name'])  # 子项物料描述
        ws.cell(row=row, column=16, value=item['quantity'])  # 子项数量
        ws.cell(row=row, column=17, value=item['unit'])  # 子项单位
        row += 1
    
    # 保存文件
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx')
    wb.save(temp_file.name)
    temp_file.close()
    
    return jsonify({
        'success': True,
        'message': 'BOM表生成成功',
        'file_path': temp_file.name
    })

@app.route('/api/download_bom/<path:file_path>')
def download_bom(file_path):
    try:
        return send_file(file_path, as_attachment=True, download_name='BOM表.xlsx')
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/api/recipe', methods=['POST'])
def create_recipe():
    data = request.json
    recipe = Recipe(
        recipe_name=data['name'],
        description=data['description']
    )
    db.session.add(recipe)
    db.session.commit()
    
    # 添加配方项
    for item in data['items']:
        recipe_item = RecipeItem(
            recipe_id=recipe.id,
            material_code=item['material_code'],
            material_name=item['material_name'],
            quantity=item['quantity'],
            unit=item['unit'],
            line_number=item['line_number'],
            project_category=item['project_category']
        )
        db.session.add(recipe_item)
    
    db.session.commit()
    return jsonify({'success': True, 'id': recipe.id})

@app.route('/api/recipe/template')
def download_recipe_template():
    """下载配方导入模板"""
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "配方导入模板"
    
    # 设置列宽
    column_widths = [15, 20, 30, 15, 15, 15]
    for i, width in enumerate(column_widths, 1):
        ws.column_dimensions[openpyxl.utils.get_column_letter(i)].width = width
    
    # 表头
    headers = ['行号', '物料编码', '物料名称', '数量', '单位', '类别']
    for col, header in enumerate(headers, 1):
        cell = ws.cell(row=1, column=col, value=header)
        cell.font = Font(bold=True)
        cell.alignment = Alignment(horizontal='center', vertical='center')
    
    # 示例数据
    example_data = [
        ['0010', 'M001', '原材料A', 2.5, 'KG', 'L'],
        ['0020', 'M002', '原材料B', 5, 'PCS', 'L'],
        ['0030', 'M003', '原材料C', 1.5, 'M', 'L']
    ]
    
    for row_idx, row_data in enumerate(example_data, 2):
        for col_idx, value in enumerate(row_data, 1):
            ws.cell(row=row_idx, column=col_idx, value=value)
    
    # 保存文件
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx')
    wb.save(temp_file.name)
    temp_file.close()
    
    return send_file(temp_file.name, as_attachment=True, download_name='配方导入模板.xlsx')

@app.route('/api/recipe/import', methods=['POST'])
def import_recipe():
    """导入配方"""
    if 'file' not in request.files:
        return jsonify({'success': False, 'message': '没有选择文件'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'success': False, 'message': '没有选择文件'}), 400
    
    try:
        # 读取Excel文件
        wb = openpyxl.load_workbook(file)
        ws = wb.active
        
        # 获取配方名称和描述
        recipe_name = request.form.get('recipe_name', '导入的配方')
        recipe_description = request.form.get('recipe_description', '从Excel导入的配方')
        
        # 创建配方
        recipe = Recipe(
            recipe_name=recipe_name,
            description=recipe_description
        )
        db.session.add(recipe)
        db.session.commit()
        
        # 读取配方项
        items = []
        for row in range(2, ws.max_row + 1):  # 从第2行开始（跳过表头）
            line_number = ws.cell(row=row, column=1).value
            material_code = ws.cell(row=row, column=2).value
            material_name = ws.cell(row=row, column=3).value
            quantity = ws.cell(row=row, column=4).value
            unit = ws.cell(row=row, column=5).value
            project_category = ws.cell(row=row, column=6).value or 'L'
            
            if all([line_number, material_code, material_name, quantity, unit]):
                recipe_item = RecipeItem(
                    recipe_id=recipe.id,
                    material_code=str(material_code),
                    material_name=str(material_name),
                    quantity=float(quantity),
                    unit=str(unit),
                    line_number=str(line_number),
                    project_category=str(project_category)
                )
                db.session.add(recipe_item)
                items.append(recipe_item)
        
        db.session.commit()
        
        return jsonify({
            'success': True, 
            'message': f'配方导入成功，共导入 {len(items)} 个配方项',
            'recipe_id': recipe.id
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': f'导入失败：{str(e)}'}), 400

@app.route('/api/recipe/export/<int:recipe_id>')
def export_recipe(recipe_id):
    """导出配方到Excel"""
    recipe = Recipe.query.get(recipe_id)
    if not recipe:
        return jsonify({'success': False, 'message': '配方不存在'}), 404
    
    items = RecipeItem.query.filter_by(recipe_id=recipe_id).order_by(RecipeItem.line_number).all()
    
    # 创建Excel文件
    wb = openpyxl.Workbook()
    ws = wb.active
    # 过滤sheet名称中的无效字符
    safe_title = "".join(c for c in recipe.recipe_name if c not in r'\/:*?"<>|')
    ws.title = safe_title[:31] if len(safe_title) > 31 else safe_title  # Excel sheet名称最大31字符
    
    # 设置列宽
    column_widths = [15, 20, 30, 15, 15, 15]
    for i, width in enumerate(column_widths, 1):
        ws.column_dimensions[openpyxl.utils.get_column_letter(i)].width = width
    
    # 配方信息
    ws.cell(row=1, column=1, value='配方名称：')
    ws.cell(row=1, column=2, value=recipe.recipe_name)
    ws.cell(row=2, column=1, value='配方描述：')
    ws.cell(row=2, column=2, value=recipe.description or '')
    
    # 表头
    headers = ['行号', '物料编码', '物料名称', '数量', '单位', '类别']
    for col, header in enumerate(headers, 1):
        cell = ws.cell(row=4, column=col, value=header)
        cell.font = Font(bold=True)
        cell.alignment = Alignment(horizontal='center', vertical='center')
    
    # 配方项数据
    for row_idx, item in enumerate(items, 5):
        ws.cell(row=row_idx, column=1, value=item.line_number)
        ws.cell(row=row_idx, column=2, value=item.material_code)
        ws.cell(row=row_idx, column=3, value=item.material_name)
        ws.cell(row=row_idx, column=4, value=item.quantity)
        ws.cell(row=row_idx, column=5, value=item.unit)
        ws.cell(row=row_idx, column=6, value=item.project_category)
    
    # 保存文件
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx')
    wb.save(temp_file.name)
    temp_file.close()
    
    return send_file(temp_file.name, as_attachment=True, download_name=f'{recipe.recipe_name}.xlsx')

@app.route('/api/recipe/export_all')
def export_all_recipes():
    """批量导出所有配方到单个表格"""
    try:
        # 获取所有活跃的配方
        recipes = Recipe.query.filter_by(is_active=True).order_by(Recipe.recipe_name).all()
        
        if not recipes:
            return jsonify({'error': '没有找到可导出的配方'}), 404
        
        # 创建工作簿
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "所有配方"
        
        # 设置列宽
        column_widths = [20, 40, 15, 20, 30, 15, 15, 20]
        for i, width in enumerate(column_widths, 1):
            ws.column_dimensions[openpyxl.utils.get_column_letter(i)].width = width
        
        # 表头 A-H列：配方名称、配方描述、行号、物料编码、物料名称、数量、单位、类别
        headers = ['配方名称', '配方描述', '行号', '物料编码', '物料名称', '数量', '单位', '类别']
        for col, header in enumerate(headers, 1):
            cell = ws.cell(row=1, column=col, value=header)
            cell.font = Font(bold=True)
            cell.alignment = Alignment(horizontal='center', vertical='center')
        
        # 数据行
        row = 2
        for recipe in recipes:
            # 获取配方项
            items = RecipeItem.query.filter_by(recipe_id=recipe.id).order_by(RecipeItem.line_number).all()
            
            # 为每个配方项创建一行数据
            for item in items:
                ws.cell(row=row, column=1, value=recipe.recipe_name)  # A列：配方名称
                ws.cell(row=row, column=2, value=recipe.description or '')  # B列：配方描述
                ws.cell(row=row, column=3, value=item.line_number)  # C列：行号
                ws.cell(row=row, column=4, value=item.material_code)  # D列：物料编码
                ws.cell(row=row, column=5, value=item.material_name)  # E列：物料名称
                ws.cell(row=row, column=6, value=item.quantity)  # F列：数量
                ws.cell(row=row, column=7, value=item.unit)  # G列：单位
                ws.cell(row=row, column=8, value=item.project_category)  # H列：类别
                row += 1
        
        # 保存文件
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx')
        wb.save(temp_file.name)
        temp_file.close()
        
        return send_file(temp_file.name, as_attachment=True, download_name='所有配方.xlsx')
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400





@app.route('/api/download_batch_bom/<path:file_path>')
def download_batch_bom(file_path):
    """下载批量生成的BOM文件"""
    try:
        # 修复文件路径问题
        if file_path.startswith('C:'):
            # 处理Windows路径
            file_path = file_path.replace('C:', 'C:\\')
        elif file_path.startswith('C%3A'):
            # 处理URL编码的路径
            file_path = file_path.replace('C%3A', 'C:\\')
        
        # 确保文件存在
        if not os.path.exists(file_path):
            return jsonify({'error': '文件不存在'}), 404
            
        return send_file(file_path, as_attachment=True, download_name='批量BOM表.xlsx')
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/bom/batch_generate_table', methods=['POST'])
def batch_generate_bom_from_table():
    """从弹窗表格数据批量生成BOM"""
    try:
        data = request.json
        bom_data = data.get('bom_data', [])
        
        if not bom_data:
            return jsonify({'success': False, 'message': '没有提供BOM数据'}), 400
        
        bom_items = []
        errors = []
        
        for item in bom_data:
            # 检查必填字段
            if not all([item.get('parent_material_code'), item.get('parent_material_name'), 
                       item.get('basic_quantity'), item.get('basic_unit'), item.get('recipe_names')]):
                errors.append(f"第{item.get('line_number', '?')}行：必填字段不完整")
                continue
            
            # 验证数量
            try:
                basic_quantity = float(item['basic_quantity'])
                if basic_quantity <= 0:
                    errors.append(f"第{item.get('line_number', '?')}行：基本数量必须大于0")
                    continue
            except:
                errors.append(f"第{item.get('line_number', '?')}行：基本数量必须是数字")
                continue
            
            # 查找配方ID
            recipe_ids = []
            for recipe_name in item['recipe_names']:
                recipe = Recipe.query.filter_by(recipe_name=recipe_name, is_active=True).first()
                if recipe:
                    recipe_ids.append(recipe.id)
                else:
                    errors.append(f"第{item.get('line_number', '?')}行：配方'{recipe_name}'不存在")
                    break
            
            if len(recipe_ids) != len(item['recipe_names']):
                continue
            
            # 添加到BOM项目列表
            bom_items.append({
                'parent_material_code': str(item['parent_material_code']),
                'parent_material_name': str(item['parent_material_name']),
                'basic_quantity': basic_quantity,
                'basic_unit': str(item['basic_unit']),
                'recipe_ids': recipe_ids,
                'remark': item.get('notes', '')
            })
        
        if errors:
            return jsonify({
                'success': False, 
                'message': f'生成失败，发现 {len(errors)} 个错误',
                'errors': errors
            }), 400
        
        if not bom_items:
            return jsonify({'success': False, 'message': '未找到有效的BOM数据'}), 400
        
        # 生成所有BOM的Excel文件
        wb_result = openpyxl.Workbook()
        ws_result = wb_result.active
        ws_result.title = "批量BOM表"
        
        # 确保只有一个工作表
        while len(wb_result.sheetnames) > 1:
            wb_result.remove(wb_result.sheetnames[-1])
        
        print(f"DEBUG: 创建工作簿，工作表数量: {len(wb_result.sheetnames)}")
        print(f"DEBUG: 工作表名称: {wb_result.sheetnames}")
        
        # 设置列宽 (A-Q列)
        column_widths = [15, 10, 20, 20, 30, 15, 10, 10, 10, 15, 15, 15, 20, 30, 15, 15, 15]
        for i, width in enumerate(column_widths, 1):
            ws_result.column_dimensions[openpyxl.utils.get_column_letter(i)].width = width
        
        # 表头 (A-Q列)
        headers = ['字段名称', '工厂', 'BOM可选文本', '父项物料号', '物料名称', '生效日期', 
                   'BOM用途', '可选BOM', 'BOM状态', '基本数量', '基本单位', '行项目号', 
                   '项目类别', '子项物料号', '子项物料描述', '子项数量', '子项单位']
        
        for col, header in enumerate(headers, 1):
            cell = ws_result.cell(row=1, column=col, value=header)
            cell.font = Font(bold=True)
            cell.alignment = Alignment(horizontal='center', vertical='center')
        
        # 数据行
        row = 2
        
        for bom_item in bom_items:
            # 为每个父物料重新开始计数
            bom_counter = 0
            
            # 获取所有选中的配方信息
            all_items = []
            
            for recipe_id in bom_item['recipe_ids']:
                recipe = Recipe.query.get(recipe_id)
                if recipe:
                    items = RecipeItem.query.filter_by(recipe_id=recipe_id).order_by(RecipeItem.line_number).all()
                    # 为每个配方项添加配方信息
                    for item in items:
                        all_items.append({
                            'recipe_name': recipe.recipe_name,
                            'recipe_description': recipe.description,
                            'line_number': item.line_number,
                            'material_code': item.material_code,
                            'material_name': item.material_name,
                            'quantity': item.quantity,
                            'unit': item.unit,
                            'project_category': item.project_category
                        })
            
            # 按配方名称排序
            all_items.sort(key=lambda x: x['recipe_name'])
            
            # 为每个BOM项生成数据行
            current_recipe = None
            
            for item in all_items:
                # 如果是新配方，更新计数器
                if current_recipe != item['recipe_name']:
                    current_recipe = item['recipe_name']
                    bom_counter += 1
                
                # 每行都填写完整的数据
                ws_result.cell(row=row, column=1, value='')  # 字段名称
                ws_result.cell(row=row, column=2, value='P060')  # 工厂
                ws_result.cell(row=row, column=3, value=item['recipe_description'])  # BOM可选文本
                ws_result.cell(row=row, column=4, value=bom_item['parent_material_code'])  # 父项物料号
                ws_result.cell(row=row, column=5, value=bom_item['parent_material_name'])  # 物料名称
                ws_result.cell(row=row, column=6, value='')  # 生效日期
                ws_result.cell(row=row, column=7, value='1')  # BOM用途
                ws_result.cell(row=row, column=8, value=f"{bom_counter:02d}")  # 可选BOM
                ws_result.cell(row=row, column=9, value='01')  # BOM状态
                ws_result.cell(row=row, column=10, value=bom_item['basic_quantity'])  # 基本数量
                ws_result.cell(row=row, column=11, value=bom_item['basic_unit'])  # 基本单位
                ws_result.cell(row=row, column=12, value=item['line_number'])  # 行项目号
                ws_result.cell(row=row, column=13, value=item['project_category'])  # 项目类别
                ws_result.cell(row=row, column=14, value=item['material_code'])  # 子项物料号
                ws_result.cell(row=row, column=15, value=item['material_name'])  # 子项物料描述
                ws_result.cell(row=row, column=16, value=item['quantity'])  # 子项数量
                ws_result.cell(row=row, column=17, value=item['unit'])  # 子项单位
                
                row += 1
        
        # 保存文件
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx')
        wb_result.save(temp_file.name)
        temp_file.close()
        
        return jsonify({
            'success': True,
            'message': f'成功生成 {len(bom_items)} 个BOM表！',
            'file_path': temp_file.name,
            'bom_count': len(bom_items)
        })
        
    except Exception as e:
        return jsonify({'success': False, 'message': f'批量生成失败：{str(e)}'}), 400

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        
        # 初始化一些示例数据
        if not Recipe.query.first():
            recipe = Recipe(recipe_name='标准配方1', description='标准产品配方')
            db.session.add(recipe)
            db.session.commit()
            
            items = [
                RecipeItem(recipe_id=recipe.id, material_code='M001', material_name='原材料A', 
                          quantity=2.5, unit='KG', line_number='0010', project_category='L'),
                RecipeItem(recipe_id=recipe.id, material_code='M002', material_name='原材料B', 
                          quantity=5, unit='PCS', line_number='0020', project_category='L'),
            ]
            for item in items:
                db.session.add(item)
            
            db.session.commit()
    
    app.run(host='0.0.0.0', port=5000, debug=True)
