#!/usr/bin/python
# -*- coding: UTF-8 -*-

'''
kysec_set -n exectl -v verified ./HttpServerWithUpload.py
nohup python HttpServerWithUpload.py > /dev/null 2>&1 &
运行命令： python2 HttpServer.py
在浏览器中输入： http://127.0.0.1:1234/
'''
__version__ = "0.6"
__all__ = ["SimpleHTTPRequestHandler"]

import os, sys, platform, socket, struct, json
import posixpath
import BaseHTTPServer
import urllib, urllib2
import urlparse
import cgi
import shutil
import mimetypes

try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO
import time
from SocketServer import ThreadingMixIn
import re
import threading
import md5, hashlib


class ToDo:
    # 获取IP地址
    def get_ip_address(ifname=None):
        if sys.platform == 'win32':
            return socket.getaddrinfo(socket.gethostname(), None, socket.AF_INET, socket.SOCK_DGRAM)[-1][4][0]
        else:
            import fcntl
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            return socket.inet_ntoa(fcntl.ioctl(
                s.fileno(),
                0x8915,  # SIOCGIFADDR
                struct.pack('256s', ifname[:15])
            )[20:24])

    def getip(self):
        try:
            myip = get_ip_address(ifname="eth0")
        except Exception, e:
            myip = "127.0.0.1"
        return myip

    # 获取系统时间
    def getTimeNow(self):
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + "-->"

    # 获取port
    def showTips(self):
        port = 1234
        try:
            print
            ToDo().getTimeNow() + 'Please visit files or dirs use Chrome Browser:http://' + ToDo().getip() + ':' + str(
                port)
        except Exception, e:
            print
            ToDo().getTimeNow() + 'You have not give a port, plase use Chrome Browser:http://' + ToDo().getip() + ':' + str(
                port)
        if not 1024 < port < 65535:  port = 1234
        return ('', port)

    # 处理文件大小
    def sizeof_fmt(self, num):
        if num == 0:
            return '0.0bytes'
        for x in ['bytes', 'KB', 'MB', 'GB']:
            if num < 1024.0:
                return "%3.1f%s" % (num, x)
            num /= 1024.0
        return "%3.1f%s" % (num, 'TB')

    # 处理文件时间
    def modification_date(self, filename):
        if os.path.isfile(filename):
            return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(os.path.getmtime(filename)))
        elif os.path.isdir(filename):
            return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(os.path.getmtime(filename)))
        else:
            return ""

    # 处理文件MD5值
    def sumfile(self, fobj):
        m = md5.new()
        while True:
            d = fobj.read(8096)
            if not d:
                break
            m.update(d)
        return m.hexdigest()

    def md5sum(self, fname):
        if fname == '-':
            ret = self.sumfile(sys.stdin)
        else:
            try:
                f = file(fname, 'rb')
            except:
                return ''
            ret = self.sumfile(f)
            f.close()
        return ret
        # 转码

    def do_utf82gbk(self, sts):
        osType = platform.system()
        if osType == "Windows":
            sts = sts.decode('utf-8').encode('gbk')
            print
            "do_utf82gbk char:" + sts
            return sts
        else:
            sts = sts
            return sts

    def do_gbk2utf8(self, sts):
        osType = platform.system()
        if osType == "Windows":
            sts = sts.decode('gbk').encode('utf-8')
            # print "do_gbk2utf8 char:" + sts
            return sts
        else:
            sts = sts
            return sts


class View:
    def do_buildHeadMessage(self, f, title):
        f.write(
            '<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd"><html>\n<head><STYLE><!--H1 {font-family: Tahoma, Arial, sans-serif;color: white;background-color: #525D76;font-size: 22px;}H2 {font-family: Tahoma, Arial, sans-serif;color: white;background-color: #525D76;font-size: 16px;}H3 {font-family: Tahoma, Arial, sans-serif;color: white;background-color: #525D76;font-size: 14px;}BODY {font-family: Tahoma, Arial, sans-serif;color: black;background-color: white;}B {font-family: Tahoma, Arial, sans-serif;color: white;background-color: #525D76;}P {font-family: Tahoma, Arial, sans-serif;background: white;color: black;font-size: 12px;}A {color: black;}A.name {color: black;}HR {color: #525D76;}--></STYLE>')
        f.write('<title>%s</title>\n' % title)
        self.do_buildJS(f)
        f.write('</head>\n')

    def do_buildJS(self, f):
        f.write('<script type="text/javascript">')
        f.write(
            "function callBackMD5(murl,domId){http.get({url:murl,timeout:100000},function(err,result){document.getElementById(domId).innerHTML=result;});}\n")
        f.write("var http = {};\n")
        f.write("http.quest = function (option, callback) {\n")
        f.write("    var url = option.url;\n")
        f.write("    var method = option.method;\n")
        f.write("    var data = option.data;\n")
        f.write("    var timeout = option.timeout || 0;\n")
        f.write("    var xhr = new XMLHttpRequest();\n")
        f.write("    (timeout > 0) && (xhr.timeout = timeout);\n")
        f.write("    xhr.onreadystatechange = function () {\n")
        f.write("        if (xhr.readyState == 4) {\n")
        f.write("            if (xhr.status >= 200 && xhr.status < 400) {\n")
        f.write("            var result = xhr.responseText;\n")
        f.write("            try {result = JSON.parse(xhr.responseText);} catch (e) {}\n")
        f.write("                callback && callback(null, result);\n")
        f.write("            } else {\n")
        f.write("                callback && callback('status: ' + xhr.status);\n")
        f.write("            }\n")
        f.write("        }\n")
        f.write("    }.bind(this);\n")
        f.write("    xhr.open(method, url, true);\n")
        f.write("    if(typeof data === 'object'){\n")
        f.write("        try{\n")
        f.write("            data = JSON.stringify(data);\n")
        f.write("        }catch(e){}\n")
        f.write("    }\n")
        f.write("    xhr.send(data);\n")
        f.write("    xhr.ontimeout = function () {\n")
        f.write("        callback && callback('timeout');\n")
        f.write("        console.log('%c连%c接%c超%c时', 'color:red', 'color:orange', 'color:purple', 'color:green');\n")
        f.write("    };\n")
        f.write("};\n")
        f.write("http.get = function (url, callback) {\n")
        f.write("    var option = url.url ? url : { url: url };\n")
        f.write("    option.method = 'get';\n")
        f.write("    this.quest(option, callback);\n")
        f.write("};\n")
        f.write("http.post = function (option, callback) {\n")
        f.write("    option.method = 'post';\n")
        f.write("    this.quest(option, callback);\n")
        f.write("};\n")
        f.write('</script>')


class SimpleHTTPRequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    server_version = "SimpleHTTP/" + __version__

    def returnMessage(self, r, info):
        f = StringIO()
        View().do_buildHeadMessage(f, '消息提示')
        f.write('<body>\n<h1>消息提示</h1>\n<HR size="1" noshade="noshade">\n')
        if r:
            f.write('<strong>成功:</strong>\n<font color="GREEN">' + info + '</font>\n')
        else:
            f.write('<strong>失败:</strong>\n<font color="RED">' + info + '</font>\n')
        f.write(' <a href="javascript:" onclick="self.location=document.referrer;">返回</a>\n')
        f.write(
            " <input type=\"button\" value=\"返回首页\" onClick=\"location='/'\">\n<HR size=\"1\" noshade=\"noshade\">\n<h2>Powered By kanbuxiaqu@outlook.com</h2>\n</body>\n</html>")
        length = f.tell()
        f.seek(0)
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=%s" % "utf-8")
        self.send_header("Content-Length", str(length))
        self.end_headers()
        if f:
            self.copyfile(f, self.wfile)
            f.close()

    def returnalert(self, r, info):
        f = StringIO()
        f.write(info)
        length = f.tell()
        f.seek(0)
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=%s" % "utf-8")
        self.send_header("Content-Length", str(length))
        self.end_headers()
        if f:
            self.copyfile(f, self.wfile)
            f.close()

    def do_GET(self):
        """Serve a GET request."""
        if ("?delete=" in self.path):
            r, info = self.deal_delFile(self.path)
            self.returnMessage(r, info)
        elif ("?getMD5=" in self.path):
            r, info = self.deal_getMD5(self.path)
            self.returnalert(r, info)
        elif ("?makedir=" in self.path):
            r, info = self.deal_makeDir(self.path)
            self.returnMessage(r, info)
        else:
            f = self.send_head()
            if f:
                try:
                    self.copyfile(f, self.wfile)
                finally:
                    f.close()

    def do_POST(self):
        r, info = self.deal_post_data()
        self.returnMessage(r, info)

    def do_HEAD(self):
        f = self.send_head()
        if f:
            f.close()

    def deal_makeDir(self, path):
        dirname = path.split('?makedir=', 1)[1]
        dirpath = self.translate_path(self.path)
        path = posixpath.normpath(urllib.unquote(dirpath + ToDo().do_utf82gbk(urllib.unquote(dirname))))
        path = path.strip()
        path = path.rstrip("\\")
        isExists = os.path.exists(path)
        if not isExists:
            os.makedirs(path)
            return (True, ToDo().do_gbk2utf8(path) + " 创建成功")
        else:
            return (False, ToDo().do_gbk2utf8(path) + " 目录已存在")

    def deal_delFile(self, path):
        if ("?delete=" in path):
            dirname = path.split('?delete=', 1)[1]
            dirpath = self.translate_path(self.path)
            path = posixpath.normpath(urllib.unquote(dirpath + dirname))
            path = path.strip()
            path = path.rstrip("\\")
        if os.path.isfile(path):
            try:
                os.remove(path)
                return (True, "文件删除成功.")
            except Exception, e:
                return (False, "文件删除失败.\n" + e)
        elif os.path.isdir(path):
            for item in os.listdir(path):
                itempath = os.path.join(path, item)
                self.deal_delFile(itempath)
            try:
                os.rmdir(path)
                return (True, "文件删除成功.")
            except Exception, e:
                return (False, "文件删除失败.\n" + e)

    def deal_getMD5(self, path):
        if ("?getMD5=" in path):
            dirname = path.split('?getMD5=', 1)[1]
            dirpath = self.translate_path(self.path)
            path = posixpath.normpath(urllib.unquote(dirpath + dirname))
            path = path.strip()
            path = path.rstrip("\\")
        if os.path.isfile(path):
            try:
                return (True, "" + ToDo().md5sum(path))
            except Exception, e:
                return (False, "文件MD5值计算失败." + e)
        elif os.path.isdir(path):
            return (False, "文件MD5值计算失败." + e)

    def deal_post_data(self):
        boundary = self.headers.plisttext.split("=")[1]
        remainbytes = int(self.headers['content-length'])
        line = self.rfile.readline()
        remainbytes -= len(line)
        if not boundary in line:
            return (False, "Content NOT begin with boundary")
        line = self.rfile.readline()
        remainbytes -= len(line)
        fn = re.findall(r'Content-Disposition.*name="file"; filename="(.*)"', line)
        if not fn:
            return (False, "Can't find out file name...")
        path = self.translate_path(self.path)
        try:
            fn = os.path.join(path, ToDo().do_utf82gbk(fn[0]))
        except Exception, e:
            return (False, "文件名请不要用中文，或者使用IE上传中文名的文件。" + e)
        while os.path.exists(fn):
            fn += "_"
        line = self.rfile.readline()
        remainbytes -= len(line)
        line = self.rfile.readline()
        remainbytes -= len(line)
        try:
            out = open(fn, 'wb')
        except IOError:
            return (False, "Can't create file to write, do you have permission to write?")
        preline = self.rfile.readline()
        remainbytes -= len(preline)
        while remainbytes > 0:
            line = self.rfile.readline()
            remainbytes -= len(line)
            if boundary in line:
                preline = preline[0:-1]
                if preline.endswith('\r'):
                    preline = preline[0:-1]
                out.write(preline)
                out.close()
                return (True, "File %s upload success!" % ToDo().do_gbk2utf8(fn))
            else:
                out.write(preline)
                preline = line
        return (False, "Unexpect Ends of data.")

    def send_head(self):
        path = self.translate_path(self.path)
        f = None
        if os.path.isdir(path):
            parts = urlparse.urlsplit(self.path)
            if not parts.path.endswith('/'):
                # redirect browser - doing basically what apache does
                self.send_response(301)
                new_parts = (parts[0], parts[1], parts[2] + '/',
                             parts[3], parts[4])
                new_url = urlparse.urlunsplit(new_parts)
                self.send_header("Location", new_url)
                self.end_headers()
                return None
            for index in "index.html", "index.htm":
                index = os.path.join(path, index)
                if os.path.exists(index):
                    path = index
                    break
            else:
                return self.list_directory(path)
        ctype = self.guess_type(path)
        try:
            # Always read in binary mode. Opening files in text mode may cause
            # newline translations, making the actual size of the content
            # transmitted *less* than the content-length!
            f = open(path, 'rb')
        except IOError:
            self.send_error(404, "File not found:" + path)
            return None
        try:
            self.send_response(200)
            self.send_header("Content-type", ctype)
            fs = os.fstat(f.fileno())
            self.send_header("Content-Length", str(fs[6]))
            self.send_header("Last-Modified", self.date_time_string(fs.st_mtime))
            self.end_headers()
            return f
        except:
            f.close()
            raise

    def list_directory(self, path):
        try:
            list = os.listdir(path)
        except os.error:
            self.send_error(404, "No permission to list directory")
            return None
        list.sort(key=lambda a: a.lower())
        f = StringIO()
        displaypath = cgi.escape(urllib.unquote(self.path))
        View().do_buildHeadMessage(f, '文件列表 ' + ToDo().do_gbk2utf8(displaypath))
        f.write("<body>\n<h1>文件列表 %s</h1>\n" % ToDo().do_gbk2utf8(displaypath))
        f.write('<HR size="1" noshade="noshade">\n')
        f.write('<table><tr><td>')
        f.write("<input type=\"button\" value=\"返回\" onClick=\"javascript:history.back(-1);\"></td><td>")
        f.write("<form ENCTYPE=\"multipart/form-data\" method=\"post\">")
        f.write("<input name=\"file\" type=\"file\"/>")
        f.write("<input type=\"submit\" value=\"上传\"/>")
        f.write("</form></td><td>")
        f.write('<form method="get">')
        f.write('<input type="text" name="makedir" />')
        f.write('<input type="submit" value="新建文件夹" />  ')
        f.write("<input type=\"button\" value=\"返回首页\" onClick=\"location='/'\">")
        f.write('</form></td></tr></table>')
        f.write('<HR size="1" noshade="noshade">')
        f.write(
            '<table border=0 width="100%" cellspacing="0" cellpadding="5" align="center" style="overflow: scroll;word-break: keep-all"><tr bgcolor="#00DB00"><td>序号</td><td>文件名</td><td>文件大小</td><td>文件创建时间</td><td>MD5</td><td>操作</td></tr>')
        idn = 1
        for name in list:
            fullname = os.path.join(path, name)
            colorName = linkname = name
            # Append / for directories or @ for symbolic links
            filename = os.getcwd() + displaypath + name
            filesize = 0
            if os.path.isfile(filename):
                filesize = os.path.getsize(filename)
            elif os.path.isdir(filename):
                filesize = os.path.getsize(filename)
            else:
                print
                ToDo().getTimeNow() + 'The file can`t read it:' + filename
            if (idn % 2 == 0):
                f.write('<tr>')
            else:
                f.write('<tr bgcolor="#eeeeee">')
            emd5 = "<a id=a_%d onclick=callBackMD5('?getMD5=%s','a_%d')>MD5</a>" % (idn, urllib.quote(linkname), idn)
            if os.path.isdir(fullname):
                colorName = '<span style="background-color: #CEFFCE;">' + name + '/</span>'
                linkname = name + "/"
                emd5 = ''
            if os.path.islink(fullname):
                colorName = '<span style="background-color: #FFBFFF;">' + name + '@</span>'
                emd5 = ''
                # Note: a link to a directory displays with @ and links with /
            f.write(
                '<td width="10%%">%d</td><td width="30%%"><a href="%s">%s</a></td><td width="20%%">%s</td><td width="20%%">%s</td><td width="50%%">%s</td><td><a href="%s">删除</a></td></tr>\n'
                % (idn, urllib.quote(linkname), ToDo().do_gbk2utf8(colorName),
                   ToDo().sizeof_fmt(filesize), ToDo().modification_date(filename), emd5,
                   "?delete=" + urllib.quote(linkname)))
            idn = idn + 1
        list = []
        f.write(
            '</table>\n<HR size="1" noshade="noshade">\n<h2>Powered By kanbuxiaqu@outlook.com</h2>\n</body>\n</html>\n')
        length = f.tell()
        f.seek(0)
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=%s" % "utf-8")
        self.send_header("Content-Length", str(length))
        self.end_headers()
        return f

    def translate_path(self, path):
        # abandon query parameters
        path = path.split('?', 1)[0]
        path = path.split('#', 1)[0]
        # Don't forget explicit trailing slash when normalizing. Issue17324
        trailing_slash = path.rstrip().endswith('/')
        path = posixpath.normpath(urllib.unquote(path))
        words = path.split('/')
        words = filter(None, words)
        path = os.getcwd()
        for word in words:
            if os.path.dirname(word) or word in (os.curdir, os.pardir):
                # Ignore components that are not a simple file/directory name
                continue
            path = os.path.join(path, word)
        if trailing_slash:
            path += '/'
        return path

    def copyfile(self, source, outputfile):
        shutil.copyfileobj(source, outputfile)

    def guess_type(self, path):
        base, ext = posixpath.splitext(path)
        if ext in self.extensions_map:
            return self.extensions_map[ext]
        ext = ext.lower()
        if ext in self.extensions_map:
            return self.extensions_map[ext]
        else:
            return self.extensions_map['']

    if not mimetypes.inited:
        mimetypes.init()  # try to read system mime.types
    extensions_map = mimetypes.types_map.copy()
    extensions_map.update({
        '': 'application/octet-stream',  # Default
        '.py': 'text/plain',
        '.c': 'text/plain',
        '.h': 'text/plain',
    })


class ThreadingServer(ThreadingMixIn, BaseHTTPServer.HTTPServer):
    pass


def test(HandlerClass=SimpleHTTPRequestHandler,
         ServerClass=BaseHTTPServer.HTTPServer):
    BaseHTTPServer.test(HandlerClass, ServerClass)


if __name__ == '__main__':
    # test()
    # 单线程
    # srvr = BaseHTTPServer.HTTPServer(serveraddr, SimpleHTTPRequestHandler)
    # 多线程
    srvr = ThreadingServer(ToDo().showTips(), SimpleHTTPRequestHandler)
    srvr.serve_forever()