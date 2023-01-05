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
        while True:
            _cur = pyperclip.paste()
            if _cur != cur:
                cur = _cur
                res += " " + cur.replace("\r", "").replace("\n", " ").replace("ﬁ", "fi")
                QproDefaultConsole.clear()
                QproDefaultConsole.print(
                    Panel("[bold green]" + res + "[/]", title="当前记录", width=_width)
                )
            if kb.is_pressed(finishCopy):
                break
            elif kb.is_pressed(cancelCopy):
                return None
            time.sleep(0.05)
        return res.strip()

    # 监听粘贴板
    with QproDefaultConsole.status("监听记录中...") as status:
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
