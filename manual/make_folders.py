import os


services = ["netflix", "amazonprime", "hulu", "disneyplus", "tiktok", "youtube", "twitch", "google drive", "dropbox", "fast", "box"]


def make_folders():

	# 上のディレクトリに移動
	os.chdir('../')

	# src ディレクトリを作成
	os.makedirs('data', exist_ok=True)

	# data ディレクトリに移動
	os.chdir('data')
    
	for service in services:
		os.makedirs(f'{service}/pcap', exist_ok=True)
		os.makedirs(f'{service}/pkt_csv', exist_ok=True)
		os.makedirs(f'{service}/flow_csv', exist_ok=True)

	return


if __name__ == '__main__':
    make_folders()