import os

def SetProxy():
    os.system('networksetup -setwebproxy Wi-Fi 127.0.0.1 8890')
    os.system('networksetup -setsecurewebproxy Wi-Fi 127.0.0.1 8890')
def DisableProxy():
    os.system('networksetup -setwebproxystate Wi-Fi off')
    os.system('networksetup -setsecurewebproxystate Wi-Fi off')