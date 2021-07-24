

## 利用fastapi自带docs的nginx配置面板

### 部署

+ **要求服务器环境**
  + 能够连接外网
  + 有dokcer环境

+ **部署过程**
  1. 首先将压缩包上传至服务器(sftp等方法)
  2. 使用命令`docker build . -t my-nginx`构建一个镜像
  3. 使用命令`docker run -d -p 80:80 -p 8000:8000 my-nginx`
  4. 然后直接通过访问`<服务器ip>:8000/docs`即可访问本面板(启动容器时会自动启动)
  
  ![image-20210724152524666](C:\Users\lzd\AppData\Roaming\Typora\typora-user-images\image-20210724152524666.png)

### 反向代理部分

+ 反向代理主要提供三个功能

  1. **查询**当前网站路径下反向代理的配置情况

     可以通过选项选择查询功能,也可以在完成配置后的响应体中的`currunt_set_proxy`字段中看到当前的配置情况

     ![](https://gitee.com/lzd-1230/img-host/raw/master/image/20210724003304.png)

     ==请求体部分使用默认值即可,最终执行结果如下==

     ![](https://gitee.com/lzd-1230/img-host/raw/master/image/20210724003417.png)

  2. **增加**反向代理的条目并自动更新服务器配置

  + 在请求体中输入请求路径和反向代理服务器ip即可

       ![](https://gitee.com/lzd-1230/img-host/raw/master/image/20210724110044.png)

       ==仅支持一个反向代理服务器的设置,如果输入了其他内容或者添加了多个服务器ip,会收到报错提示==

  + 异常处理的返回提示

    + 输入不满足ip地址格式

       ![](https://gitee.com/lzd-1230/img-host/raw/master/image/20210724110323.png)

    + 添加了多次
    
       ![image-20210724110344628](C:\Users\lzd\AppData\Roaming\Typora\typora-user-images\image-20210724110344628.png)

  3. **删除**反向代理条目并自动更新服务器配置

     + 现根据查询当前路径反向代理服务器的ip,然后在choice中选择后输入对应ip即可删除配置

       ​	![image-20210724110843658](C:\Users\lzd\AppData\Roaming\Typora\typora-user-images\image-20210724110843658.png)

       得到的响应

       ![image-20210724110814293](C:\Users\lzd\AppData\Roaming\Typora\typora-user-images\image-20210724110814293.png)

       如果输入错误的ip则会返回错误,并提示现在配置的ip

       ![](https://gitee.com/lzd-1230/img-host/raw/master/image/20210724110629.png)

### 测试

+ 通过`docker run --name proxy_test nginx`启动一个容器(ip:172.17.0.4)

+ 将测试页面内容`proxy_test`放入测试服务器中

+ 在面板中配置所起容器的ip地址

  1. 查询是否有配置了反向代理

     ![image-20210724151549182](C:\Users\lzd\AppData\Roaming\Typora\typora-user-images\image-20210724151549182.png)

   2. 若没有则可以添加我们要配置的容器ip

      ![image-20210724151705444](C:\Users\lzd\AppData\Roaming\Typora\typora-user-images\image-20210724151705444.png)

  3. 若发现返回如下,则证明配置成功且没有语法错误

     ![image-20210724151747900](C:\Users\lzd\AppData\Roaming\Typora\typora-user-images\image-20210724151747900.png)

  4. 最终访问我们所配置的服务器`http://172.22.161.106/`

     ![image-20210724151813772](C:\Users\lzd\AppData\Roaming\Typora\typora-user-images\image-20210724151813772.png)


### 重定向部分

+ regular填重定向的地址,可以以指定的正则形式,也可以直接写简单的路径。这里以/abc为例

+ path填入重定向后需要访问的文件路径

  ![](https://gitee.com/lzd-1230/img-host/raw/master/image/20210724150258.png)

如果格式正确,则会在请求后自动写入并重新加载配置文件

![image-20210724150610436](C:\Users\lzd\AppData\Roaming\Typora\typora-user-images\image-20210724150610436.png)

访问该地址,则可以看到被重定向到我们指定的目录下的acb目录下,默认是index.html文件

![image-20210724150703919](C:\Users\lzd\AppData\Roaming\Typora\typora-user-images\image-20210724150703919.png)

## 总结

+ 不足
  + 反向代理部分仅实现了一台反向代理服务器的配置,未能实现upstream那种可以配置多个反向代理的功能。
  + 重定向部分仅实现了最基本的url路径的完全匹配的重定向，未能测试其它很多的正则，以及配置方面的错误输入等容错还未实现

+ 学习总结

  + 通过一年的红岩新生培训,也算是从啥都不会，到了解了一些运维的知识与内容,但是越了解越觉得自己差的多，还是要好好努力多实践，多做，多学习!从这次考核实现过程中很多文件操作等等内容都极其不熟练,导致时间浪费，最终功能实现的得不是很全面。
  + 最后感谢一下xuanchen哥哥每一次的关键技术指导，才使得我能完成这些功能555

  