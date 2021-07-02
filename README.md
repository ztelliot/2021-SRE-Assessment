# 2021-SRE-Assessment

运维方向考核提交点

**请提交到自己选择的题目的对应分支**

## 运维暑假考核

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

### 备注

要求：语言不限 实现方式不限 但 **不得抄袭** 

**任选一题 限时一周 即7月25日 00:30分截止**

**做完请提交整个项目 PR 到选题对应的分支**

描述写清自己 **选择的题目**  **运行的环境** **详尽的Readme**（如 编译 部署 运行 已知的bug）

https://github.com/ztelliot/2021-SRE-Assessment

有问题发邮件到 zhuxuanchen@redrock.team
