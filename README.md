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
bash pcap2csv.sh service_name video_type
```

## Dataset
[Raw dataset](https://drive.google.com/drive/folders/17dYY7POuN2-8fTw8hxO6VPtW8BD2Lvdm?usp=sharing)

An each filename in the above includes service labels.

~~A dataset on a flow basis, which includes OSINT (Open Source INTelligence) data and Routing Infomation data, will be public soon.~~

[Flow dataset](https://drive.google.com/drive/folders/1UFEem5v-rOZEFKexTe8wqmMqWK6osmwV?usp=drive_link)

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


## Flow dataset attributes
- srcip: client machine's IP address
- dstip: server machine's IP address
- proto: protocol number
- bytes_r/s: transmitted traffic volume from server to client / client to server
- bytes_r_max: maximum flow volume of BoF (Bag-of-Flows, aggregated with 4-tuple(srcip, dstip, proto, dstport=443).)
- first: session start time
- last: session end time
- pkts_r/s: transmitted traffic volume from server to client / client to server
- count: the number of flows within BoF
- ss_time: session duration
- loss, recon_loss, kl_loss: output of our model
- sni: server name indication
- osint_asn: AS number obtained　from [Shodan](https://www.shodan.io/)
- cn: common name obtained　from [Shodan](https://www.shodan.io/)
- san: subject alternative name obtained　from [Shodan](https://www.shodan.io/)
- org: organization name obtained　from [Shodan](https://www.shodan.io/)
- net: prefix obtained　from our BGP RIB
- osint_service: serivice name tied with osint data
- sid: service identification (1: netflix, 2: AmazonPrimeVideo, 3: YouTube, 4: Hulu, 5: Disneyplus, 6: Twitch, 7: TikTok)
- osint_sid: sid indentified by osint data
