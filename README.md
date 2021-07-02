# 2021-SRE-Assessment

运维方向考核提交点

**请提交到自己选择的题目的对应分支**

## 运维暑假考核

> 以下题目任选其一完成，进阶非必须，仅举例

### Q1 Web服务器管理

> 尽管nginx设置起来已经很简单了，但谁又嫌面板多呢？

#### 基础要求

##### 1. 反向代理等静态网站的管理

##### 2. 常用操作的管理 例如 重定向

##### 3. 容器化

#### 进阶要求

##### 1. 集群部署

##### 2. 友好的Web交互界面

##### 3. 网站SSL管理

##### 4. 动态网站管理

##### 5. 日志展示

##### 6. ......

> 不限Web服务器类型， traefik nginx tengine apache caddy 甚至是 kubernetes svc 和 iis

#### 参考

- [traefik](https://doc.traefik.io/traefik/)

- [svc](https://kubernetes.io/docs/concepts/services-networking/service/#services-without-selectors)

- [nginx](http://nginx.org/en/docs/)

- [tengine](https://tengine.taobao.org/documentation.html)

- [apache](http://httpd.apache.org/docs/)

- [caddy](https://caddyserver.com/docs/)

### Q2 邮件管理程序

> 很多时候我们都需要向用户发送邮件，但对于需要群发的邮件，手动发送总是令人恼火，所以，我们希望有一个程序来管理邮件发送

#### 基础要求

##### 1. 通过SMTP发送邮件

##### 2. 邮件编辑

##### 3. 管理收件人，批量发送邮件

##### 4. 容器化

#### 进阶要求

##### 1. 集群部署

##### 2. 友好的Web交互界面

##### 3. 添加附件、发送HTML格式邮件

##### 4. 定时发送邮件

##### 5. 提供API以方便其他程序调用

##### 6. 支持其他邮件发送协议

##### 7. ......

### Q3 备份中台

> 一个生产环境不能没有备份，但对于一个大型集群，手动一个一个 Application 备份总是令人烦躁的也是不优雅的，那么，用一个备份中台来统一管理备份任务无疑是件很优雅的事

#### 基础要求

##### 1. K8s 各种资源的备份

##### 2. 备份 PVC 的数据

##### 3. 定时进行备份

##### 4. 支持常见服务备份，例如 mysql

#### 进阶要求

##### 1. 使用自定义脚本备份

##### 2. 提供多种备份储存

##### 3. 还原数据

##### 4. ......

> 灵活的使用 K8s 的 Cronjob 可以解决大部分问题

#### 参考

- [cronjob](https://kubernetes.io/docs/concepts/workloads/controllers/cron-jobs/)

- [velero](https://github.com/vmware-tanzu/velero)

### Q4 自选

如果你觉得上述题目小菜一碟，你可以自由选题，于7月18日0点之前将选题提交审核，审核通过就可以开始你的表演了

### 备注

上述题目均欢迎自由补充

要求：语言不限 实现方式不限 但 **不得抄袭** 

**任选一题 限时一周 即7月25日 00:30分截止**

**做完请提交整个项目 PR 到选题对应的分支**

描述写清自己 **选择的题目**  **运行的环境** **详尽的Readme**（如 编译 部署 运行 已知的bug）

https://github.com/ztelliot/2021-SRE-Assessment

有问题发邮件到 zhuxuanchen@redrock.team
