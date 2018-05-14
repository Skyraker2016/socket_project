## 用户-服务器：

方法 | 用途 | 用户端格式 | 服务器格式
:--- | :--- | :--- | :--- |
INIT | 初始化用户（上线时） | `INIT_<INITLIST>`。其中，`<INITLIST>`格式为：`{<FILENAME>:<FILESIZE>, ...}` | `INITACK`
GET | 请求下载 | `GET_<FILENAME>` | 成功：`SUCCESS_<FILESIZE>_<GETLIST>`，其中`<GETLIST>`为`{(<IP>>,<PORT>):(<BEGIN_INDEX>,<END_INDEX>), ...}`；失败：`ERROR_<ERROR_TYPE>`
ADD | 添加文件(一般在完成下载后) | `ADD_<FILENAME>_<FILESIZE>` | `ADDACK`
QUIT | 下线 | `QUIT` | `QUITACK`

## 用户-用户：
方法 | 用途 | 请求方格式 | 响应方格式
:--- | :--- | :--- | :--- |
DOWNLOAD | 请求下载 | `DOWNLOAD_<FILENAME>_(<BEGIN_INDEX>,<END_INDEX>)` | 先返回`DOWNLOADACK_<FILESIZE>`（此时的文件大小为待传输的大小）,再开始传输`<INDEX>_<DATA>`


*TODO*
1. P2P聊天功能
2. 传输验证
3. 并行下载、上传
4. 进度条