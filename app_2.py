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
        create_entity(class_name, package, j['column'], d)
        file_name = make_targz()
        msg = '文件已生成，请查阅～'

    return render_template('create_class_2.html', msg=msg, file_name=file_name)


def Python2JavaType(python_type, value):
    if python_type == 'str':
        return 'String'
    elif python_type == 'int':
        return 'Int'
    elif python_type == 'list':
        Item = value[0]
        ItemType = Python2JavaType(type(Item).__name__, Item)
        return 'MutableList<{}>'.format(ItemType)
    else:
        return 'String'


def create_sub_entity(class_name, package, columns, date):
    properties = ''
    if columns:
        for idx, key in enumerate(columns.keys()):
            split = ',' if idx < (len(columns) - 1) else ''
            typeName = type(columns[key]).__name__
            itemType = Python2JavaType(typeName, columns[key])
            properties += 'val %s: %s' % (key, itemType) + split + '\n\t'
    c = {'package': package,
         'class_name': class_name,
         'properties': properties,
         'date': date}

    s = render_template('entity_templates.html', **c)
    create_java_file(class_name, package, s)


# 创建entity
def create_entity(class_name, package, columns, date):
    properties = ''
    if columns:
        for idx, key in enumerate(columns.keys()):
            split = ',' if idx < (len(columns) - 1) else ''
            columnType = 'String'
            typename = type(columns[key]).__name__
            if typename == 'str':
                columnType = 'String'
            elif typename == 'list':
                item = columns[key][0]
                columnType = 'MutableList<{}>'.format(upper_str(key))
                create_sub_entity(upper_str(key), package, item, date)

            properties += 'val %s: %s' % (key, columnType) + split + '\n\t'

    c = {'package': package,
         'class_name': class_name,
         'properties': properties,
         'date': date}

    s = render_template('entity_templates.html', **c)
    create_java_file(class_name, package, s)


# 将首字母转换为大写
def upper_str(s):
    if len(s) <= 1:
        return s
    return (s[0:1]).upper() + s[1:]


# 创建kotlin文件
def create_java_file(class_name, package, text, suffix='.kt'):
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
