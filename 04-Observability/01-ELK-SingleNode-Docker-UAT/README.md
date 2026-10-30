The diagram illustrates the architecture of a Docker Compose monitoring stack named monitoring, which consists of eight services organized into four Docker networks. The Monitoring Network contains Grafana, which displays dashboards, and Prometheus, which collects metrics; the Logging Network contains Elasticsearch, which stores and indexes data, Kibana, which lets users search and visualize logs, and Logstash, which processes and forwards log events; the Cache Network contains Redis, a key-value store, and RedisInsight, its web-based management interface; and the Tracing Network contains Zipkin, which collects and visualizes distributed traces. The services communicate through Docker network aliases and internal container ports, while published ports allow users to access their web interfaces from the host, such as Grafana on port 3000, Kibana on 5601, Prometheus on 9090, and Zipkin on 9411. Two named volumes, esdata1 and grafana-storage, preserve Elasticsearch and Grafana data when containers are recreated. Overall, this architecture brings metrics, logs, caching, and distributed tracing together in one environment, while the Compose configuration defines how services start, connect, and store data.

<img width="900" height="500" alt="elk-compose -v1" src="https://github.com/user-attachments/assets/ddc0cc74-557d-478d-8e82-2120e2db72a1" />

## Docker Compose configuration for the monitoring stack.

# check config file: 
```sh
docker compose -f docker-compose-elk-singlenode-UAT.yml config
```
# pull images: 
```sh
docker compose -f docker-compose-elk-singlenode-UAT.yml pull
```
# Start: 
```sh
docker compose -f docker-compose-elk-singlenode-UAT.yml up -d
```
# Check status: 
```sh
docker compose -f docker-compose-elk-singlenode-UAT.yml ps
```
<img width="1404" height="957" alt="image" src="https://github.com/user-attachments/assets/640be8b9-f96e-43ad-9586-0150eac39e7c" />

# View logs: 
```sh
docker compose -f docker-compose-elk-singlenode-UAT.yml logs -f <service>
```
#
## SECURITY WARNING:
Elasticsearch security is disabled and Grafana uses admin/admin.
Use only in a trusted development environment unless access is secured.
Published ports may be reachable from other machines.

### Set IP hostname in DNS
C:\Windows\System32\drivers\etc\hosts
IP Name
192.168.x.x elk

## ZIPKIN
```sh
docker logs zipkin
```
check UI: http://elk:9411/
<img width="1434" height="742" alt="image" src="https://github.com/user-attachments/assets/38e5e248-85eb-46ef-a206-9a223983b840" />

## Redis insight
check UI: http://elk:5540/
<img width="1440" height="829" alt="image" src="https://github.com/user-attachments/assets/d3619b67-321c-4963-85d4-7b9546c08cc6" />

# add redis database
<img width="1427" height="835" alt="image" src="https://github.com/user-attachments/assets/21cb248a-2a08-4d94-9636-12cff8a2a745" />

<img width="1421" height="866" alt="image" src="https://github.com/user-attachments/assets/46495d61-08ed-49c4-9b32-b9578449f6eb" />

<img width="1429" height="805" alt="image" src="https://github.com/user-attachments/assets/fe0d9598-7dc4-4026-9517-c66b87aab3a3" />

# load Sample data
<img width="1425" height="844" alt="image" src="https://github.com/user-attachments/assets/d26cf71f-cc47-4b50-ae4f-5d4979f2b99d" />

## Prometheus
```sh
docker logs prometheus
```
<img width="1441" height="586" alt="image" src="https://github.com/user-attachments/assets/6b3cd517-3c16-46d5-aaa8-1f367ac40107" />

## Grafana
<img width="1433" height="783" alt="image" src="https://github.com/user-attachments/assets/229172b8-b4a3-4c89-8981-d83498f319f1" />

# Add new data source
<img width="1421" height="859" alt="image" src="https://github.com/user-attachments/assets/0140b4d4-a95c-4f09-8183-7eb051241e33" />

<img width="1430" height="603" alt="image" src="https://github.com/user-attachments/assets/5ffa682f-091a-407a-8d0d-de7e8b0b170f" />

## check Kibana
kibana is not secure

<img width="854" height="883" alt="image" src="https://github.com/user-attachments/assets/ec3b4b9a-20ee-4f57-a59a-54c529e12cf6" />



