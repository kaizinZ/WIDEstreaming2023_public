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
source .bashrc
```

Move to the 'manual' directory and create a directory to save the generated pcap files.
```
python3 make_folder.py
```

Operate the program and then watch the videos, refer to streaming.py for the arguments.
```
python3 streaming.py -s netflix -u user_name -t anime
```

Convert pcap files to csv.
```
sh pcap2csv.sh netflix anime
```

# Dataset
The dataset will be published once completed.