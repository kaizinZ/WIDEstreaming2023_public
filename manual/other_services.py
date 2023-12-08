import os
import random
import argparse
import time
import subprocess
import string

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options


#並列プロセス実行数の最大値
max_process = 4

parser = argparse.ArgumentParser()
parser.add_argument('-t', '--type', choices=['download', 'upload', 'both'], required=True)
parser.add_argument('-u', '--user', type=str, default='')
parser.add_argument('-s', '--service', required=True, choices=["google_drive", "dropbox", "fast", "box"])
#parser.add_argument('-f', '--file', type=str)
parser.add_argument('-p', '--profile', type=int, default=0)
parser.add_argument('-o', '--offset', type=int, default=0)

services = ["google_drive", "dropbox", "fast", "box"]


def make_driver(user_name, profile):
    options = Options()
    # プロファイルの保存先を指定
    options.add_argument(f"--user-data-dir=/home/{user_name}/.config/google-chrome")
    options.add_argument(f"--profile-directory=Profile {profile}")

    # ChromeDriverのパス
    driver_path = "../chromedriver"

    # パスを通していない場合
    if os.path.isfile(driver_path):
        # WebDriver インスタンスの作成
        driver = webdriver.Chrome(options=options, executable_path=driver_path)
    else:
        # パスを通している場合
        driver = webdriver.Chrome(options=options)
    
    return driver
    

def generate_file_name(service_name: str, action_type: str, offset=0):
    os.chdir(f'../data/{service_name}/pcap')
    pcap_path = os.getcwd()

    # ディレクトリ内の全てのファイルとサブディレクトリをリスト化
    all_files = os.listdir(pcap_path)
    
    # ビデオタイプごとにファイルだけをカウント
    tp_files = [1 for f in all_files if os.path.isfile(os.path.join(pcap_path, f)) and action_type in f]
    file_count = sum(tp_files)
    
    return f'{service_name}_{action_type}_{file_count}.pcap'


def main():
    args = parser.parse_args()
    action_type = args.type
    user_name = args.user
    service_name = args.service
    profile = args.profile

    # ファイルの数によって名前をインクリメント netflix_0 -> netflix_1
    file_name = generate_file_name(service_name, action_type)

    print(file_name)
    
    # 自動的にchromeを開く
    driver = make_driver(user_name=user_name, profile=profile)
    driver.get('https://www.google.com')

    # TCPDUMP
    command = f'sudo tcpdump -p -w {file_name} -i ens160 -Z {user_name} -W 1'
    print(command)

    tcpdump_process = subprocess.Popen(command.split(' '))
    
    try:
        time.sleep(1e4) # 動作完了を待つ 
    except KeyboardInterrupt: 
        tcpdump_process.terminate()
        tcpdump_process.wait()  # プロセスが完全に終了するのを待つ
        print("tcpdump stopped.")
    
    # 自動でChromeを落とす
    #time.sleep(exec_min*60)
    driver.quit()

if __name__ == '__main__':
    main()