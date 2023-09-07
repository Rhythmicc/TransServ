import os
import json
from QuickProject import user_root, user_lang, QproDefaultConsole, QproInfoString, _ask

enable_config = True
config_path = os.path.join(user_root, ".TransServ_config")

questions = {
    "finishCopy": {
        "type": "input",
        "message": "设置完成复制的按键",
        "default": "f2",
    },
    "cancelCopy": {
        "type": "input",
        "message": "设置取消复制的按键",
        "default": "esc",
    },
}


def init_config():
    with open(config_path, "w") as f:
        basic_config = {i: _ask(questions[i]) for i in questions}
        basic_config.update({
            "actions": [
                ["keyboard", ".ctrl", "v"]
            ]
        })
        json.dump(
            basic_config, f, indent=4, ensure_ascii=False
        )
    QproDefaultConsole.print(
        QproInfoString,
        f'Config file has been created at: "{config_path}"'
        if user_lang != "zh"
        else f'配置文件已创建于: "{config_path}"',
    )


class TransServConfig:
    def __init__(self):
        if not os.path.exists(config_path):
            init_config()
        with open(config_path, "r") as f:
            self.config = json.load(f)

    def select(self, key):
        if key not in self.config and key in questions:
            self.update(key, _ask(questions[key]))
        return self.config[key]

    def update(self, key, value):
        self.config[key] = value
        with open(config_path, "w") as f:
            json.dump(self.config, f, indent=4, ensure_ascii=False)
