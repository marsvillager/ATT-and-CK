# 1、安装

```
pip install autopep8
```

# 2、配置

文件（file）-设置（settings）-工具(tools)-外部工具(external-tools)-添加

- 名称：autopep8（随便）

- 程序：autopep8

- 实参：--in-place --aggressive --aggressive $FilePath$

- 工作目录：$ProjectFileDir$

- 输出筛选器：$FILE_PATH$\:$LINE$\:$COLUMN$\:.*