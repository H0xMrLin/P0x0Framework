#0x0Framework<br />
此框架基于WSGI (This framework base in python WSGI)<br />
如果要运行在实际环境还要用uwsgi运行:<br />
运行代码：<br />
uwsgi --http :8080 --wsgi-file manage.py <br />
 (根据实际需求修改端口号和uwsgi参数)<br />
若为生产环境请直接：python3 manage.py [Port]<br />
 诺不设置Port参数 实际运行端口为8080<br />
采用MVC架构，当然也可以直接跨界就View和Dal 但可能会导致不安全<br />
默认后台入口为 http://127.0.0.1:[port]/adminx 用户名useradmin 密码为2020password<br />
 mime.json 为响应的mime的json文件 <br />
<br />
<br />
基本目录介绍<br />
├─Bll (业务逻辑层)<br />
├─Dal (数据库层)<br />
├─Lib (依赖文件)<br />
│ ├─dbC (数据库模型连接文件)<br />
├─sqliteDB (存储db文件)<br />
├─static (静态文件夹)<br />
│ └─admin (默认后台的静态文件)<br />
├─View (视图层)<br />
│ ├─admin (默认后台视图)<br />
│ ├─_Template (模板文件夹)<br />
│ │ └─admin<br />
└─__pycache__<br />
<br />
基本目录详细:<br />
├─Bll (业务逻辑层)<br />
├─Dal (数据库层)<br />
│ └─__pycache__<br />
├─Lib (依赖文件)<br />
│ ├─dbC<br />
│ │ └─__pycache__<br />
│ └─__pycache__<br />
├─sqliteDB (存储db文件)<br />
├─static (静态文件夹)<br />
│ └─admin (默认后台的静态文件)<br />
│ ├─api<br />
│ ├─css<br />
│ │ └─themes<br />
│ ├─images<br />
│ ├─js<br />
│ │ └─lay-module<br />
│ │ ├─echarts<br />
│ │ ├─iconPicker<br />
│ │ ├─layarea<br />
│ │ ├─layuimini<br />
│ │ ├─step-lay<br />
│ │ ├─tableSelect<br />
│ │ ├─treetable-lay<br />
│ │ └─wangEditor<br />
│ │ └─fonts<br />
│ ├─lib<br />
│ │ ├─font-awesome-4.7.0<br />
│ │ │ ├─css<br />
│ │ │ ├─fonts<br />
│ │ │ ├─less<br />
│ │ │ └─scss<br />
│ │ ├─jq-module<br />
│ │ │ └─zyupload<br />
│ │ ├─jquery-3.4.1<br />
│ │ └─layui-v2.5.5<br />
│ │ ├─css<br />
│ │ │ └─modules<br />
│ │ │ ├─laydate<br />
│ │ │ │ └─default<br />
│ │ │ └─layer<br />
│ │ │ └─default<br />
│ │ ├─font<br />
│ │ ├─images<br />
│ │ │ └─face<br />
│ │ └─lay<br />
│ │ └─modules<br />
│ └─page<br />
│ └─table<br />
├─View<br />
│ ├─admin<br />
│ │ └─__pycache__<br />
│ ├─_Template<br />
│ │ └─admin<br />
│ └─__pycache__<br />
└─__pycache__
