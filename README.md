# TransServ

监听粘贴板内容并自动拷贝翻译结果。

![example](https://cos.rhythmlian.cn/ImgBed/579ccb0a5e33aca05e88ee5928524788.png)

## 安装

```shell
pip3 install git+https://github.com/Rhythmicc/TransServ.git -U
```

## 使用

```shell
ts # 查看帮助
ts serv   # 启动服务
sudo ts serv --auto_paste # 在Mac上启动服务，翻译完成后自动粘贴
```

1. 默认监听中可以连续复制文本，复制完毕后按下`f2`表示复制完毕并进行翻译、按下`esc`表示取消当前记录。
2. 修改按键方式，修改`~/.TransServ_config`中的内容。
3. 支持翻译完成后自定义动作，修改配置表中的`actions`内容，程序将按顺序执行：

```json
"actions": [
    ["keyboard", ".cmd", ".ctrl", "v"], // 各种组合键, '.'开头表示特殊键，组合键长度不限
    ["mouse", "left", 1],               // 鼠标操作，支持 left/right/middle，1表示点击次数
    ["sleep", 0.5],                     // 延时，单位秒
]
```

## 注意

1. 使用本插件需要配置 [QuickStart_Rhy](https://github.com/Rhythmicc/qs) 库中的翻译引擎，支持`Alapi`、`腾讯云`、`DeepL`。（推荐使用 DeepL，翻译结果更好；你可以在海鲜市场购买一个 DeepL 的 API 账号）
2. Mac 用户需要 sudo 权限以允许本脚本监听键盘事件
3. 当你把 Mac 的 `caps` 键用作输入法切换键时，keyboard库会错误识别 `key_name`，因此需要进行如下修改：

    ```python
    # 修改 keyboard 库中的 _darwinkeyboard.py 的handler方法：在第376行后添加如下内容：
    if key_name is None:
        return None
    ```
