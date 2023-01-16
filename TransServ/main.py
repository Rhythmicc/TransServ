from QuickProject.Commander import Commander
from . import *

app = Commander("ts")


@app.command()
def serv(auto_paste: bool = False):
    """
    启动服务
    Start service

    :param auto_paste: 是否自动粘贴翻译结果
    """
    import re
    import time
    import pyperclip
    import keyboard as kb
    from pynput import keyboard
    from pynput.keyboard import Key
    from rich.panel import Panel
    from QuickStart_Rhy import system
    from QuickStart_Rhy.api import translate
    from QuickProject import QproErrorString

    _width = QproDefaultConsole.width
    finishCopy = config.select("finishCopy")
    cancelCopy = config.select("cancelCopy")
    keyboard_controller = keyboard.Controller()

    def record():
        res = ""
        cur = pyperclip.paste()
        replace_table = {
            re.escape("\r"): "",
            re.escape("\n"): " ",
            re.escape("ﬁ"): "fi",
            re.escape("ﬂ"): "fl",
            re.escape("ﬀ"): "ff",
            re.escape("ﬃ"): "ffi",
            re.escape("ﬄ"): "ffl",
            re.escape("ﬅ"): "ft",
            re.escape("ﬆ"): "st",
        }
        pattern = re.compile("|".join(replace_table.keys()))

        is_busy = False

        while True:
            _cur = pyperclip.paste()
            if _cur != cur:
                is_busy = True
                cur = _cur
                res += " " + pattern.sub(
                    lambda m: replace_table[re.escape(m.group(0))], cur
                )
                external_exec("say 已记录", __no_wait=True)
                QproDefaultConsole.clear()
                QproDefaultConsole.print(
                    Panel("[bold green]" + res + "[/]", title="当前记录", width=_width)
                )
            if kb.is_pressed(finishCopy):
                external_exec("say 完成记录", __no_wait=True)
                break
            elif kb.is_pressed(cancelCopy):
                external_exec("say 取消记录", __no_wait=True)
                QproDefaultConsole.clear()
                return None
            time.sleep(0.05 if is_busy else 1.5)
        return res.strip()

    # 监听粘贴板
    with QproDefaultStatus("监听记录中...") as status:
        while True:
            if ct := record():
                status.update("正在翻译...")
                retry = 3
                while (res := translate(ct)) and (not res or res == "[ERROR] 请求失败了"):
                    retry -= 1
                    if retry < 0:
                        QproDefaultConsole.print(QproErrorString, "翻译失败，请检查网络连接或API有效性")
                    time.sleep(1)

                if res and res != "[ERROR] 请求失败了":
                    pyperclip.copy(res)
                    if auto_paste:
                        keyboard_controller.press(
                            Key.cmd if system.startswith("darwin") else Key.ctrl
                        )
                        keyboard_controller.press("v")
                        keyboard_controller.release("v")
                        keyboard_controller.release(
                            Key.cmd if system.startswith("darwin") else Key.ctrl
                        )

                    QproDefaultConsole.clear()
                    QproDefaultConsole.print(
                        Panel(
                            "[bold]"
                            + ct
                            + "[/]\n"
                            + "-" * (_width - 4)
                            + "\n[bold green]"
                            + res
                            + "[/]",
                            title="[bold magenta]原文 + 译文[/]",
                            width=_width,
                        )
                    )
                    QproDefaultConsole.print(QproInfoString, "翻译完成, 已复制到粘贴板")
                else:
                    QproDefaultConsole.clear()
                status.update("监听记录中...")


def main():
    """
    注册为全局命令时, 默认采用main函数作为命令入口, 请勿将此函数用作它途.
    When registering as a global command, default to main function as the command entry, do not use it as another way.
    """
    app()


if __name__ == "__main__":
    main()
