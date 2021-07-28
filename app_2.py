# -*- coding: UTF-8 -*-


import os
import json
import time
import tarfile
from flask import Flask, render_template, send_from_directory, request

app = Flask(__name__)


@app.route("/")
def index2():
    return render_template('create_class_2.html')


@app.route("/download/<filename>", methods=['GET'])
def downloader(filename):
    # 指定文件下载目录，默认为当前项目根路径
    dirpath = os.path.join(app.root_path, '')
    # as_attachment=True 表示下载
    return send_from_directory(dirpath, filename, as_attachment=True)


@app.route('/createClass', methods=['GET', 'POST'])
def create_class():
    file_name = msg = None
    fields = request.form['fields']
    if len(fields) <= 0:
        msg = 'request data json is null!'
    print(fields)
    j = json.loads(fields, encoding='utf-8')
    class_name = j['class']
    package = j['package']
    if len(class_name) <= 0:
        msg = 'className is null!'
    if len(package) <= 0:
        msg = 'package is null'
    print(class_name + '\n' + package)
    if not msg or len(msg) <= 0:
        d = time.strftime("%Y-%m-%d", time.localtime())

        print('--- create entity class')
        create_KotlinAndJava(class_name, package, j['column'], d)
        create_swift(class_name, package, j['column'], d)
        file_name = make_targz()
        msg = '文件已生成，请查阅～'

    return render_template('create_class_2.html', msg=msg, file_name=file_name)


def Python2JavaType(python_type, value, fileType='java'):
    if python_type == 'str':
        return 'String'
    elif python_type == 'int':
        return 'Int'
    elif python_type == 'list':
        Item = value[0]
        ItemType = Python2JavaType(type(Item).__name__, Item)
        if fileType.startswith('j'):
            return 'List<{}>'.format(ItemType)
        elif fileType.startswith('k'):
            return 'MutableList<{}>'.format(ItemType)
        elif fileType.startswith('s'):
            return '[{}]'.format(ItemType)
    else:
        return 'String'


def create_sub_entity(class_name, package, columns, date):
    swift_properties = java_properties = kotlin_properties = ''
    if type(columns).__name__ == 'dict':
        for idx, key in enumerate(columns.keys()):
            split = ',' if idx < (len(columns) - 1) else ''
            typeName = type(columns[key]).__name__
            kotlinItemType = Python2JavaType(typeName, columns[key], 'kotlin')
            javaItemType = Python2JavaType(typeName, columns[key], 'java')
            swiftItemType = Python2JavaType(typeName, columns[key], 'swift')
            kotlin_properties += 'val %s: %s' % (key, kotlinItemType) + split + '\n\t'
            java_properties += 'public %s %s' % (javaItemType, key) + ';' + '\n\t'
            swift_properties += 'let %s: %s' % (key, swiftItemType) + '\n\t'
    create_file_with_properties(class_name, package, kotlin_properties, date, 'kotlin_templates.html', '.kt')
    create_file_with_properties(class_name, package, java_properties, date, 'java_templates.html', '.java')
    create_file_with_properties(class_name, package, swift_properties, date, 'swift_templates.html', '.swift')


def create_file_with_properties(class_name, package, properties, date, templates, suffix):
    content = {'package': package,
               'class_name': class_name,
               'properties': properties,
               'date': date}
    s = render_template(templates, **content)
    create_entity_file(class_name, package, s, suffix)


#
def create_swift(class_name, package, columns, date):
    properties = ''
    if columns:
        for key in columns.keys():
            columnType = 'String'
            typename = type(columns[key]).__name__
            if typename == 'str':
                columnType = 'String'
            elif typename == 'list':
                item = columns[key][0]
                columnType = '[{}]'.format(upper_str(key))
                create_sub_entity(upper_str(key), package, item, date)
            properties += 'let %s: %s' % (key, columnType) + '\n\t'

    c = {'package': package,
         'class_name': class_name,
         'properties': properties,
         'date': date}
    s = render_template('swift_templates.html', **c)
    create_entity_file(class_name, package, s, '.swift')


# 创建kotlin & java
def create_KotlinAndJava(class_name, package, columns, date):
    java_properties = properties = ''
    if columns:
        for idx, key in enumerate(columns.keys()):
            split = ',' if idx < (len(columns) - 1) else ''
            javaColumnType = columnType = 'String'
            typename = type(columns[key]).__name__
            if typename == 'str':
                columnType = 'String'
            elif typename == 'list':
                item = columns[key][0]
                columnType = 'MutableList<{}>'.format(upper_str(key))
                javaColumnType = 'List<{}>'.format(upper_str(key))
                create_sub_entity(upper_str(key), package, item, date)
            elif typename == 'dict':
                for key1 in columns[key].keys():
                    item = columns[key][key1]
                    columnType = 'MutableList<{}>'.format(upper_str(key1))
                    itemType = type(item).__name__
                    if itemType == 'list':
                        create_sub_entity(upper_str(key1), package, item[0], date)
                    elif itemType == 'dict':
                        create_sub_entity(upper_str(key1), package, item, date)

            properties += 'val %s: %s' % (key, columnType) + split + '\n\t'
            java_properties += 'public %s %s' % (javaColumnType, key) + ';' + '\n\t'

    c = {'package': package,
         'class_name': class_name,
         'properties': properties,
         'date': date}

    s = render_template('kotlin_templates.html', **c)
    create_entity_file(class_name, package, s)
    # create java bean
    j = {'package': package,
         'class_name': class_name,
         'properties': java_properties,
         'date': date}
    s = render_template('java_templates.html', **j)
    create_entity_file(class_name, package, s, '.java')


# 将首字母转换为大写
def upper_str(s):
    if len(s) <= 1:
        return s
    return (s[0:1]).upper() + s[1:]


# 创建kotlin文件
def create_entity_file(class_name, package, text, suffix='.kt'):
    dirs = 'D:/temp/python/' + package.replace('.', '/') + '/'
    if not os.path.exists(dirs):
        os.makedirs(dirs, 0o777)
    fd = os.open(dirs + class_name + suffix, os.O_WRONLY | os.O_CREAT)
    os.write(fd, text.encode(encoding="utf-8", errors="strict"))
    os.close(fd)


# 生成tar.gz压缩包
def make_targz():
    file_name = 'com.tar.gz'
    source_dir = 'D:/temp/python/'
    with tarfile.open(file_name, "w:gz") as tar:
        tar.add(source_dir, arcname=os.path.basename(source_dir))
    return file_name


if __name__ == '__main__':
    app.run()
