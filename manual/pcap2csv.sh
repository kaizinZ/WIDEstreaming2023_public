#!/bin/bash

# sh pcap2csv.sh netflix movie
# のように引数を指定.
# movieの全てのpcapがcsvに変換される

# 引数の確認
if [ "$#" -ne 2 ]; then
  echo "Usage: $0 <service> <file_name>"
  exit 1
fi

service=$1
video_type=$2

# コマンドを実行するディレクトリ
input_dir="../../src/${service}/pcap"
output_dir1="../../src/${service}/pkt_csv"
output_dir2="../../src/${service}/flow_csv"

# インデックスをインクリメントしながらファイルを処理
index=0
while true; do
  # 引数から変数に値を設定
  file_name="${service}_${video_type}_${index}.pcap"
  base_name=$(basename "$file_name" .pcap)  # 拡張子を除いたファイル名

  # ファイルが存在するかチェック
  if [ ! -f "${input_dir}/${file_name}" ]; then
    echo "File ${input_dir}/${file_name} does not exist. Stopping."
    break
  fi

  # packet
  tshark -r "${input_dir}/${file_name}" -E header=y -E separator=, -T fields -e ip.src -e ip.dst -e ip.proto -e ip.hdr_len -e ip.dsfield.ecn -e ip.len -e ip.id -e ip.frag_offset -e ip.ttl -e ip.checksum -e tcp.srcport -e tcp.dstport -e tcp.hdr_len -e tcp.len -e tcp.seq -e tcp.ack -e tcp.flags.ns -e tcp.flags.fin -e tcp.window_size_value -e tcp.checksum -e tcp.urgent_pointer -e tcp.option_kind -e tcp.option_len -e tcp.options.timestamp.tsval -e tcp.options.timestamp.tsecr -e udp.srcport -e udp.dstport -e udp.length -e udp.checksum -e gquic.puflags.rsv -e tls.handshake.extensions_server_name -o "tls.keylog_file:$HOME/tls_key.log" > "${output_dir1}/${base_name}.csv"
  
  # flow
  tshark -r "${input_dir}/${file_name}" -E header=y -E separator=, -T fields -e frame.time_epoch -e ip.src -e ip.dst -e tcp.srcport -e tcp.dstport -e ip.proto -e udp.srcport -e udp.dstport -e tls.handshake.extensions_server_name -Y "tls" -o "tls.keylog_file:$HOME/tls_key.log" > "${output_dir2}/${base_name}.csv"

  # インデックスをインクリメント
  index=$((index + 1))
done