# WIDEstreaming2023_public
The goal is to collect traffic centered around streaming services and create a dataset. Considering the terms of service for each service, data collection is semi-automated. Instead of scraping or crawling, videos are played manually.

## Environment

- Ubuntu 20.04.6 LTS
- Python3 3.8.10
- selenium==4.11.2
- Google Chrome 116.0.5845.110 (64 bit)
- TShark 3.2.3 


## How to Use

You need to download the chromedriver that matches the version of Chrome.

Create a file to save the TLS key in advance and write it into bash.

```
touch /home/user/tls_key.log
echo 'export SSLKEYLOGFILE="$HOME/tls_key.log"' >> ~/.bashrc
echo 'export PATH=$PATH:/home/user/.local/bin' >> ~/.bashrc
source ~/.bashrc
```

Move to the 'manual' directory and create a directory to save the generated pcap files.
```
python3 make_folders.py
```

Operate the program and then watch the videos, refer to streaming.py for the arguments.
```
python3 streaming.py -s service_name -u user_name -t video_type
```

Convert pcap files to csv.
```
sh pcap2csv.sh service_name video_type
```

## Dataset
[Raw dataset](https://drive.google.com/drive/folders/17dYY7POuN2-8fTw8hxO6VPtW8BD2Lvdm?usp=sharing)

An each filename in the above includes service labels.

A dataset on a flow basis, which includes OSINT (Open Source INTelligence) data and Routing Infomation data, will be public soon.


## Scenario (Set by Application Type)
- Streaming
  - Video Viewing (PGC)
    - Assume video durations typical for anime (20-30 minutes), drama (40-60 minutes), and movies (around 120 minutes). Not all videos are watched in full; viewing is stopped at random times:
    - 50% of the time, stop at a random moment.
    - 50% of the time, watch the entire video.
  - Video Viewing (UGC)
    - The duration of user-generated content is unknown, hence timing is completely random:
    - YouTube:
      - Short: 0-15 minutes, completely random.
      - Live: 0-60 minutes, completely random.
      - Zapping, UGC: 0-30 minutes, completely random.
    - TikTok: 0-30 minutes, completely random.
      - Primarily short video-focused service.
      - Includes live content.
- Downloads and File System
  - File sizes range from approximately 10KB to 250MB.
  - Includes uploading, downloading, and both.
