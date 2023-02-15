const completionSpec: Fig.Spec = {
    "name": "ts",
    "description": "ts",
    "subcommands": [
        {
            "name": "complete",
            "description": "获取补全列表",
            "args": [],
            "options": [
                {
                    "name": "--team",
                    "description": "团队名",
                    "isOptional": true,
                    "args": {
                        "name": "team",
                        "description": "团队名"
                    }
                },
                {
                    "name": "--token",
                    "description": "团队token",
                    "isOptional": true,
                    "args": {
                        "name": "token",
                        "description": "团队token"
                    }
                },
                {
                    "name": "--is-script",
                    "description": "是否为脚本"
                }
            ]
        },
        {
            "name": "serv",
            "description": "启动服务\n    Start service",
            "args": [],
            "options": [
                {
                    "name": "--auto-paste",
                    "description": "是否自动粘贴翻译结果"
                },
                {
                    "name": "--disable-audio",
                    "description": "是否禁用音效"
                }
            ]
        }
    ]
};
export default completionSpec;
