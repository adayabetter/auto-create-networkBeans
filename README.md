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

####1.拿到接口的返回数据
<img width="1910" alt="t1" src="https://user-images.githubusercontent.com/13690806/126748809-e3767502-d669-4991-bd77-b6a11f6dc92f.png">




####2.配置包名，类名，字段信息
<img width="1553" alt="t2" src="https://user-images.githubusercontent.com/13690806/126748831-2fc6a12a-f1e3-440b-8100-9c04d3a3d5fd.png">



####3.点击提交，查看生成结果
<img width="1100" alt="t3" src="https://user-images.githubusercontent.com/13690806/126748973-0abad3dd-6dd1-4662-9787-809c029ff1a3.png">



####4.生成相应的Kotlin data class 文件
<img width="906" alt="t4" src="https://user-images.githubusercontent.com/13690806/126749043-2d72be72-8062-4141-a5bf-3ad5dba1bde0.png">




