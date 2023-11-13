from QuickProject.Commander import Commander
from . import *

app = Commander("ts", seg_flag=True)


@app.command()
def serv(auto_paste: bool = False, disable_audio: bool = False):
    """
    启动服务
    Start service

    :param auto_paste: 是否自动粘贴翻译结果
    :param disable_audio: 是否禁用音效
    """
    import re
    import time
    import pyperclip
    import keyboard as kb
    from pynput import keyboard
    from pynput.keyboard import Key
    from pynput import mouse
    from pynput.mouse import Button
    from rich.panel import Panel
    from QuickStart_Rhy import platform
    from QuickStart_Rhy.apiTools import translate
    from QuickProject import QproErrorString

    _width = QproDefaultConsole.width
    finishCopy = config.select("finishCopy")
    cancelCopy = config.select("cancelCopy")
    keyboard_controller = keyboard.Controller()
    mouse_controller = mouse.Controller()

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
        re.escape("ð"): "(",
        re.escape("Þ"): ")",
        re.escape("Â"): "×",
        re.escape("À"): "-",
        re.escape("¼"): "=",
    }
    pattern = re.compile("|".join(replace_table.keys()))

    def record():
        res = ""
        cur = pyperclip.paste()
        is_busy = False

        while True:
            _cur = pyperclip.paste()
            if _cur != cur:
                is_busy = True
                cur = _cur
                if not isinstance(cur, str):  # 防止出现非字符串类型
                    continue
                res += " " + pattern.sub(
                    lambda m: replace_table[re.escape(m.group(0))], cur
                )
                if not disable_audio:
                    external_exec(
                        f'afplay {os.path.join(os.path.dirname(__file__),"audio_source","recorded.mp3",)}',
                        __no_wait=True,
                    )
                QproDefaultConsole.clear()
                QproDefaultConsole.print(
                    Panel("[bold green]" + res + "[/]", title="当前记录", width=_width)
                )
            if kb.is_pressed(finishCopy) and is_busy:
                if not disable_audio:
                    external_exec(
                        f'afplay {os.path.join(os.path.dirname(__file__),"audio_source","translating.mp3",)}',
                        __no_wait=True,
                    )
                break
            elif kb.is_pressed(cancelCopy) and is_busy:
                if not disable_audio:
                    external_exec(
                        f'afplay {os.path.join(os.path.dirname(__file__),"audio_source","cancel.mp3",)}',
                        __no_wait=True,
                    )
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
                while retry:
                    retry -= 1
                    if not(res := translate(ct)):
                        continue
                    time.sleep(1)

                if res and res != "[ERROR] 请求失败了":
                    pyperclip.copy(res)
                    if auto_paste:
                        auto_action(keyboard_controller, mouse_controller, platform, Key, Button)

                    QproDefaultConsole.clear()
                    QproDefaultConsole.print(
                        Panel(
                            f"[bold]{ct}[/]\n{'-' * (_width - 4)}\n[bold green]{res}[/]",
                            title="[bold magenta]原文 + 译文[/]",
                            width=_width,
                        )
                    )
                    QproDefaultConsole.print(QproInfoString, "翻译完成, 已复制到粘贴板")
                    if not disable_audio:
                        external_exec(
                            f'afplay {os.path.join(os.path.dirname(__file__),"audio_source","complete.mp3",)}',
                            __no_wait=True,
                        )
                else:
                    QproDefaultConsole.print(QproErrorString, "翻译失败")
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
