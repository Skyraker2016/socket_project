## 报文：
方法 | 作用 | Client | Server Success | SERVER Fail
:--- | :--- | :--- | :--- | :---
GET | 请求传输文件 | `GET_<filename>` | `FILE_<filename>_<filesize>_<address>` | `ERROR FILE_NOT_FOUND`
LIST | 列出服务器拥有的文件 | `LIST` | `LIST_<{filename:filesize}>` | 
//UPLOAD | 向服务器上传文件 | `UPLOAD_FILENAME`, `ID_<index>_<data>` | `UPLOADACK` 
QUIT | 退出 | `QUIT`

TODO:
1. upload
2. index
3. md5 check