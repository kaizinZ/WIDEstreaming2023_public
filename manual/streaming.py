import os
import random
import argparse
import time
import subprocess

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options


services = ["netflix", "amazonprime", "hulu", "disneyplus", "tiktok", "youtube", "twitch"]
video_types = ['anime', 'drama', 'movie', 'ugc', 'zapping', 'live', 'short']

#並列プロセス実行数の最大値
max_process = 4

parser = argparse.ArgumentParser()
parser.add_argument('-t', '--type', choices=video_types, required=True)
parser.add_argument('-u', '--user', type=str, default='')
parser.add_argument('-s', '--service', required=True, choices=services)
#parser.add_argument('-f', '--file', type=str)
parser.add_argument('-p', '--profile', type=int, default=0)
parser.add_argument('-o', '--offset', type=int, default=0)


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


def random_stop_minutes(type: str, service_name: str):
    if service_name == 'youtube':
        if type == 'ugc':
            return  0.5 + random.random() * 30
        elif type == 'zapping':
            return  0.5 + random.random() * 30
        elif type == 'live':
            return 0.5 + random.random() * 60
        elif type == 'short':
            return 0.5 + random.random() * 15
    elif service_name == 'tiktok':
        return 0.5 + random.random() * 30
    elif service_name == 'twitch':
        return 0.5 + random.random() * 60
    else:
        if random.random() >= 0.5:
            if type == 'anime':
                return random.random() * 20
            elif type == 'drama':
                return random.random() * 40
            elif type == 'movie':
                return random.random() * 100
            else:
                print("error: argument type is unknown.")
                exit(1)
        else:
            delta = random.random()
            plus_or_minus = random.random()
            if plus_or_minus >= 0.5:
                if type == 'anime': return 20 + delta * 2
                elif type == 'drama': return 40 + delta * 4
                elif type == 'movie': return 100 + delta * 10
                else:
                    print("error: argument type is unknown.")
                    exit(1)
            else:
                if type == 'anime': return 20 - delta * 2
                elif type == 'drama': return 40 - delta * 4
                elif type == 'movie': return 100 - delta * 10
                else:
                    print("error: argument type is unknown.")
                    exit(1)
            


def generate_file_name(service_name: str, video_type: str, offset=0):
    os.chdir(f'../../src/{service_name}/pcap')
    pcap_path = os.getcwd()

    # ディレクトリ内の全てのファイルとサブディレクトリをリスト化
    all_files = os.listdir(pcap_path)
    
    # ビデオタイプごとにファイルだけをカウント
    tp_files = [1 for f in all_files if os.path.isfile(os.path.join(pcap_path, f)) and video_type in f]
    file_count = sum(tp_files)
    
    return f'{service_name}_{video_type}_{file_count}.pcap'


def short_random_play(driver, exec_min):
    """
    short動画をランダム時間で再生するための自動化
    ランダム時間でキーボードの下を入力し次の動画を再生する
    """
    # ActionChainsをインスタンス化
    action = webdriver.ActionChains(driver)

    start = time.time()
    while True:
        play_time = random.random() * 60 # 1分以内でランダム時間
        time.sleep(play_time)
        action.send_keys(Keys.DOWN).perform()
        end = time.time()
        if (end - start) / 60 >= exec_min:
            return


def zapping(driver, exec_min):
    """
    short動画をランダム時間で再生するための自動化
    ランダム時間でキーボードの下を入力し次の動画を再生する
    """
    # ActionChainsをインスタンス化
    action = webdriver.ActionChains(driver)

    start = time.time()
    while True:
        play_time = random.random() * 150 + 30 # 3分以内でランダム時間, 最低30秒
        time.sleep(play_time)
        action.key_down(Keys.SHIFT).send_keys('n').key_up(Keys.SHIFT).perform()
        end = time.time()
        if (end - start) / 60 >= exec_min:
            return
        

def main():
    args = parser.parse_args()
    video_type = args.type
    user_name = args.user
    service_name = args.service
    profile = args.profile

    # ファイルの数によって名前をインクリメント netflix_0 -> netflix_1
    file_name = generate_file_name(service_name, video_type)

    print(file_name)

    # ビデオ視聴時間をランダム化
    exec_min = random_stop_minutes(video_type, service_name)

    # 自動的にchromeを開く
    driver = make_driver(user_name=user_name, profile=profile)
    driver.get('https://www.google.com')

    # TCPDUMP
    command = f'sudo tcpdump -p -w {file_name} -i ens160 -Z {user_name} -G {exec_min*60} -W 1'
    print(command)

    tcpdump_process = subprocess.Popen(command.split(' '))
    
    if (service_name in ['tiktok', 'youtube']) and video_type == 'short':
        short_random_play(driver, exec_min)
    elif service_name == 'youtube' and video_type == 'zapping':
        zapping(driver, exec_min)
    else:
        time.sleep(exec_min*60)

    # 自動でChromeを落とす
    #time.sleep(exec_min*60)
    driver.quit()

if __name__ == '__main__':
    main()