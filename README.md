<h1 style="text-align: center"> TransServ </h1>

监听粘贴板内容并自动拷贝翻译结果。

![](https://cos.rhythmlian.cn/ImgBed/579ccb0a5e33aca05e88ee5928524788.png)

## 安装

```shell
pip3 install https://github.com/Rhythmicc/TransServ.git -U
```

## 使用

```shell
ts --help # 查看帮助
ts serv   # 启动服务
```

1. 默认监听中可以连续复制文本，复制完毕后按下`f2`表示复制完毕并进行翻译、按下`esc`表示取消当前记录。
2. 修改按键方式，修改`~/.TransServ_config`中的内容。

## 注意

1. 使用本插件需要配置 [QuickStart_Rhy](https://github.com/Rhythmicc/qs) 库中的翻译引擎，支持`Alapi`、`腾讯云`、`DeepL`。（推荐使用 DeepL，翻译结果更好；你可以在海鲜市场购买一个 DeepL 的 API 账号）
2. Mac 用户需要 sudo 权限以允许本脚本监听键盘事件
