## Client-Server型：
* Server端支持多Client同时访问，多线程服务；
* `list`方法：获得服务器文件内容
* `get filename`方法：下载名为`filename`的内容

## p2p:
* 中央服务器维护文件表
* 用户-服务器：初始化用户、请求文件表、更新文件表、用户下线，多线程服务器
* 用户-用户：请求数据、数据重排


*TODO*
1. P2P聊天功能
2. 传输验证
3. 并行下载、上传
4. 并行进度条