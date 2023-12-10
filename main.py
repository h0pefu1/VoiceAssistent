
from time import sleep
import config
import stt
import tts
from fuzzywuzzy import fuzz
import datetime
import num2words 
import webbrowser
import random
from selenium import webdriver

print(f"{config.VA_NAME} (v{config.VA_VER}) начал свою работу ...")


def va_respond(voice: str):
    print(voice)
    if voice.startswith(config.VA_ALIAS):
        # обращаются к ассистенту
        cmd = recognize_cmd(filter_cmd(voice))

        if cmd['cmd'] not in config.VA_CMD_LIST.keys():
            tts.va_speak("Что?")
        else:
            execute_cmd(cmd['cmd'])


def filter_cmd(raw_voice: str):
    cmd = raw_voice

    for x in config.VA_ALIAS:
        cmd = cmd.replace(x, "").strip()

    for x in config.VA_TBR:
        cmd = cmd.replace(x, "").strip()

    return cmd


def recognize_cmd(cmd: str):
    rc = {'cmd': '', 'percent': 0}
    for c, v in config.VA_CMD_LIST.items():

        for x in v:
            vrt = fuzz.ratio(cmd, x)
            if vrt > rc['percent']:
                rc['cmd'] = c
                rc['percent'] = vrt

    return rc


def execute_cmd(cmd: str):
    if cmd == 'help':
        # help
        text = "Я умею: ..."
        text += "произносить время ..."
        text += "и открывать браузер"
        tts.va_speak(text)
        pass
    elif cmd == 'ctime':
        # current time
        now = datetime.datetime.now()
        text = "Сейч+ас " + num2words(now.hour) + " " + num2words(now.minute)
        tts.va_speak(text)

    elif cmd == 'joke':
        jokes = ['Исскуственный интелект не захватит мир',
                 ]

        tts.va_speak(random.choice(jokes))

    elif cmd == 'open_browser':
        driver = webdriver.Chrome()
        driver.get("https://www.selenium.dev/selenium/web/web-form.html")
        driver.implicitly_wait(0.5)
        sleep(500)

# начать прослушивание команд
stt.va_listen(va_respond)