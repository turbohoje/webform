#docker volume create grafana_plugins

docker run -d \
  -p 8444:3000 \
  --name grafana \
  -v grafana_config:/etc/grafana \
  -v grafana_data:/var/lib/grafana \
  -v /home/jmeyer/webform/log.txt:/var/lib/grafana/infinity-csv/log.txt \
  -v grafana_plugins:/var/lib/grafana/plugins \
  grafana/grafana-oss:latest

