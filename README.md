auto-create-networkBeans


#### 项目介绍
本项目示例采用python语言开发，基于flask服务利用html建立基础模板，通过json数据自动生成Bean文件，如 javaBean, kotlinBean.






#### 启动服务
在根目录执行：  python3 app_2.py






#### 使用说明
1.配置需要生成的包名，如： "package": "com.example.networkdemo.bean"

2.配置根目录结构的类名，如："class": "Result"

3.配置服务端返回的字段名称，"column": “{ JsonObject}”	

可以直接将浏览器中请求到的Json数据，粘贴到column中



参考： https://gitee.com/omsgit/auto-create-java.git