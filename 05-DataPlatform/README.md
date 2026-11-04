data platform stack 

<img width="699" height="563" alt="image" src="https://github.com/user-attachments/assets/1c796a62-814c-438c-b518-8687fa1294b2" />




  cd ./data-platform/phase3
docker compose build
ls
docker images

docker ps
docker cmpose ps

docker compose up -d
docker compose ps
docker compose logs -f python-producer
find data -type f


docker compose up -d kafka
docker compose ps
docker compose logs -f kafka
docker exec kafka /opt/kafka/bin/kafka-topics.sh   --bootstrap-server localhost:9092   --create   --if-not-exists   --topic streaming-events   --partitions 3   --replication-factor 1
docker exec kafka /opt/kafka/bin/kafka-topics.sh   --bootstrap-server localhost:9092   --create   --if-not-exists   --topic raw-customers   --partitions 3   --replication-factor 1
docker exec kafka /opt/kafka/bin/kafka-topics.sh   --bootstrap-server localhost:9092   --create   --if-not-exists   --topic raw-products   --partitions 3   --replication-factor 1
docker exec kafka /opt/kafka/bin/kafka-topics.sh   --bootstrap-server localhost:9092   --create   --if-not-exists   --topic raw-orders   --partitions 3   --replication-factor 1
docker exec kafka /opt/kafka/bin/kafka-topics.sh   --bootstrap-server localhost:9092   --list
docker exec kafka /opt/kafka/bin/kafka-topics.sh   --bootstrap-server localhost:9092   --describe

docker compose build python-producer
docker compose up -d python-producer
docker compose ps
docker compose logs -f python-producer
docker exec kafka /opt/kafka/bin/kafka-console-consumer.sh   --bootstrap-server localhost:9092   --topic streaming-events   --from-beginning   --max-messages 5
docker exec kafka /opt/kafka/bin/kafka-console-consumer.sh   --bootstrap-server localhost:9092   --topic raw-customers   --from-beginning   --max-messages 3
docker compose ps
docker compose logs --tail=40 python-producer
docker exec kafka /opt/kafka/bin/kafka-topics.sh --bootstrap-server
docker exec kafka /opt/kafka/bin/kafka-topics.sh --bootstrap-server localhost:9092 --describe
docker compose ps
docker compose logs --tail=40 python-producer
docker exec kafka /opt/kafka/bin/kafka-topics.sh --bootstrap-server localhost:9092 --describe
docker exec kafka /opt/kafka/bin/kafka-console-consumer.sh   --bootstrap-server localhost:9092   --topic raw-customers   --from-beginning   --max-messages 3
docker compose logs --tail=100 python-producer | grep -E "raw-|customers|products|orders|ERROR"
docker exec kafka /opt/kafka/bin/kafka-console-consumer.sh   --bootstrap-server localhost:9092   --topic raw-customers   --from-beginning   --max-messages 3
docker exec kafka /opt/kafka/bin/kafka-console-consumer.sh   --bootstrap-server localhost:9092   --topic raw-products   --from-beginning   --max-messages 3
docker exec kafka /opt/kafka/bin/kafka-console-consumer.sh   --bootstrap-server localhost:9092   --topic raw-orders   --from-beginning   --max-messages 3
docker compose logs --tail=200 python-producer
cat app/raw_generator.py
cat .env
docker exec kafka /opt/kafka/bin/kafka-get-offsets.sh   --bootstrap-server localhost:9092   --topic raw-customers
docker exec kafka /opt/kafka/bin/kafka-get-offsets.sh   --bootstrap-server localhost:9092   --topic raw-products
docker exec kafka /opt/kafka/bin/kafka-get-offsets.sh   --bootstrap-server localhost:9092   --topic raw-orders
vi app/raw_generator.py
docker compose up -d --build --force-recreate python-producer
docker compose logs --tail=100 python-producer
docker exec kafka /opt/kafka/bin/kafka-get-offsets.sh   --bootstrap-server localhost:9092   --topic raw-orders
docker exec kafka /opt/kafka/bin/kafka-get-offsets.sh   --bootstrap-server localhost:9092   --topic raw-customers
docker exec kafka /opt/kafka/bin/kafka-get-offsets.sh   --bootstrap-server localhost:9092   --topic raw-products
docker exec kafka /opt/kafka/bin/kafka-console-consumer.sh   --bootstrap-server localhost:9092   --topic raw-customers   --from-beginning   --max-messages 3
docker exec kafka /opt/kafka/bin/kafka-console-consumer.sh   --bootstrap-server localhost:9092   --topic raw-orders   --from-beginning   --max-messages 3
docker exec kafka /opt/kafka/bin/kafka-console-consumer.sh   --bootstrap-server localhost:9092   --topic raw-products   --from-beginning   --max-messages 3


docker compose config -q
docker compose up -d seaweedfs
docker compose ps
docker compose logs --tail=100 seaweedfs
curl -i http://localhost:8333/
curl -i http://localhost:9333/cluster/status
docker run --rm --network phase3_default   -e AWS_ACCESS_KEY_ID=admin   -e AWS_SECRET_ACCESS_KEY=secret   amazon/aws-cli:latest   --endpoint-url http://seaweedfs:8333   s3 mb s3://warehouse
docker run --rm --network phase3_default   -e AWS_ACCESS_KEY_ID=admin   -e AWS_SECRET_ACCESS_KEY=secret   amazon/aws-cli:latest   --endpoint-url http://seaweedfs:8333   s3 ls
docker run --rm --network phase3_default   -e AWS_ACCESS_KEY_ID=admin   -e AWS_SECRET_ACCESS_KEY=secret   amazon/aws-cli:latest   --endpoint-url http://seaweedfs:8333   s3api head-bucket --bucket warehouse
echo "Iceberg warehouse storage test" > /tmp/iceberg-test.txt
docker run --rm --network phase3_default   -v /tmp/iceberg-test.txt:/tmp/iceberg-test.txt:ro   -e AWS_ACCESS_KEY_ID=admin   -e AWS_SECRET_ACCESS_KEY=secret   amazon/aws-cli:latest   --endpoint-url http://seaweedfs:8333   s3 cp /tmp/iceberg-test.txt s3://warehouse/validation/iceberg-test.txt
docker run --rm --network phase3_default   -e AWS_ACCESS_KEY_ID=admin   -e AWS_SECRET_ACCESS_KEY=secret   amazon/aws-cli:latest   --endpoint-url http://seaweedfs:8333   s3 ls s3://warehouse/validation/
docker compose restart seaweedfs
sleep 5

docker run --rm --network phase3_default   -e AWS_ACCESS_KEY_ID=admin   -e AWS_SECRET_ACCESS_KEY=secret   amazon/aws-cli:latest   --endpoint-url http://seaweedfs:8333   s3 ls s3://warehouse/validation/

vi docker-compose.yml
  517  docker compose config -q
docker compose up -d seaweedfs
  519  curl -i http://localhost:8181/v1/config
  520  docker run --rm --network phase3_default   -e AWS_ACCESS_KEY_ID=admin   -e AWS_SECRET_ACCESS_KEY=secret   -e AWS_DEFAULT_REGION=us-east-1   amazon/aws-cli:latest   --endpoint-url http://seaweedfs:8333   s3tables list-table-buckets
  521  curl -i   "http://localhost:8181/v1/config?warehouse=s3%3A%2F%2Fwarehouse"
  522  curl -i   "http://localhost:8181/v1/warehouse/namespaces"
  523  docker run --rm --network phase3_default   -e AWS_ACCESS_KEY_ID=admin   -e AWS_SECRET_ACCESS_KEY=secret   -e AWS_DEFAULT_REGION=us-east-1   amazon/aws-cli:latest   --endpoint-url http://seaweedfs:8333   s3tables list-table-buckets   --output json
  524  docker compose exec seaweedfs sh -c '
  525    echo "S3_TABLE_BUCKET=$S3_TABLE_BUCKET"
  526    test -n "$AWS_ACCESS_KEY_ID" && echo "AWS access key: configured"
  527    test -n "$AWS_SECRET_ACCESS_KEY" && echo "AWS secret key: configured"
  528  '
  529  docker compose logs --tail=80 seaweedfs
  530  docker compose exec seaweedfs weed shell
  531  docker compose logs --tail=50 seaweedfs
  532  docker run --rm --network phase3_default   -e AWS_ACCESS_KEY_ID=admin   -e AWS_SECRET_ACCESS_KEY=secret   -e AWS_DEFAULT_REGION=us-east-1   amazon/aws-cli:latest   --endpoint-url http://seaweedfs:8333   s3tables list-table-buckets
  533  docker run --rm --network phase3_default   python:3.12-slim   sh -c 'pip install --quiet awscurl && awscurl \
  534      --service s3 \
  535      --region us-east-1 \
  536      --access_key admin \
  537      --secret_key secret \
  538      http://seaweedfs:8181/v1/iceberg-warehouse/namespaces'
  539  curl --include   --aws-sigv4 'aws:amz:us-east-1:s3'   --user 'admin:secret'   'http://localhost:8181/v1/iceberg-warehouse/namespaces'
  540  curl --include   --aws-sigv4 'aws:amz:us-east-1:s3'   --user 'admin:secret'   --header 'Content-Type: application/json'   --request POST   --data '{"namespace":["raw"],"properties":{}}'   'http://localhost:8181/v1/iceberg-warehouse/namespaces'
  541  curl --silent --show-error   --aws-sigv4 'aws:amz:us-east-1:s3'   --user 'admin:secret'   'http://localhost:8181/v1/iceberg-warehouse/namespaces'
  542  cat docker-compose.yml
  543  vi docker-compose.yml
  544  docker compose config -q
  545  docker compose up -d seaweedfs
  546  docker compose ps seaweedfs
  547  docker compose logs --tail=40 seaweedfs
  548  curl --silent --show-error   --aws-sigv4 'aws:amz:us-east-1:s3'   --user 'admin:secret'   'http://localhost:8181/v1/iceberg-warehouse/namespaces'
  549  docker compose ps
  550  docker compose up -d kafka python-producer
  551  vi docker-compose.yml
  552  docker compose ps
  553  docker compose logs --tail=40 kafka
  554  docker compose logs --tail=40 python-producer
  555  docker compose stop python-producer
  556  docker compose exec kafka /opt/kafka/bin/kafka-topics.sh   --bootstrap-server localhost:9092   --create --if-not-exists   --topic streaming-events   --partitions 3   --replication-factor 1
  557  docker compose exec kafka /opt/kafka/bin/kafka-topics.sh   --bootstrap-server localhost:9092   --create --if-not-exists   --topic raw-customers   --partitions 3   --replication-factor 1
  558  docker compose exec kafka /opt/kafka/bin/kafka-topics.sh   --bootstrap-server localhost:9092   --create --if-not-exists   --topic raw-products   --partitions 3   --replication-factor 1
  559  docker compose exec kafka /opt/kafka/bin/kafka-topics.sh   --bootstrap-server localhost:9092   --create --if-not-exists   --topic raw-orders   --partitions 3   --replication-factor 1
  560  docker compose exec kafka /opt/kafka/bin/kafka-topics.sh   --bootstrap-server localhost:9092   --list
  561  docker compose exec kafka /opt/kafka/bin/kafka-topics.sh   --bootstrap-server localhost:9092   --describe
  562  docker compose start python-producer
  563  docker compose logs --tail=40 python-producer
  564  docker volume ls
  565  for topic in streaming-events raw-customers raw-products raw-orders; do   echo "===== $topic =====";   docker compose exec -T kafka /opt/kafka/bin/kafka-get-offsets.sh     --bootstrap-server localhost:9092     --topic "$topic"     --time -1; done
  566  docker compose exec kafka /opt/kafka/bin/kafka-console-consumer.sh   --bootstrap-server localhost:9092   --topic raw-customers   --from-beginning   --max-messages 2
  567  docker compose exec kafka /opt/kafka/bin/kafka-console-consumer.sh   --bootstrap-server localhost:9092   --topic streaming-events   --from-beginning   --max-messages 2
  568  curl -I -L   https://repo.maven.apache.org/maven2/org/apache/iceberg/iceberg-kafka-connect-runtime/1.12.0/iceberg-kafka-connect-runtime-1.12.0.zip
  569  docker compose exec kafka ls -l   /opt/kafka/bin/connect-distributed.sh
  570  docker compose exec kafka java -version
  571  curl -I -L   https://archive.apache.org/dist/iceberg/apache-iceberg-1.12.0.tar.gz
  572  curl -I -L   https://archive.apache.org/dist/iceberg/apache-iceberg-1.12.0/apache-iceberg-1.12.0.tar.gz
  573  mkdir -p downloads
  574  cd downloads
  575  wget https://archive.apache.org/dist/iceberg/apache-iceberg-1.12.0/apache-iceberg-1.12.0.tar.gz
  576  mkdir -p downloads
  577  cd downloads
  578  wget https://archive.apache.org/dist/iceberg/apache-iceberg-1.12.0/apache-iceberg-1.12.0.tar.gz
  579  ls
  580  ls -la
  581  ls -lh apache-iceberg-1.12.0.tar.gz
  582  tar -tzf apache-iceberg-1.12.0.tar.gz | head
  583  tar -xzf apache-iceberg-1.12.0.tar.gz
  584  ls
  585  rm -f apache-iceberg-1.12.0*
  586  rm -rf apache-iceberg-1.12.0*
  587  wget https://archive.apache.org/dist/iceberg/apache-iceberg-1.12.0/apache-iceberg-1.12.0.tar.gz
  588  tar -xzf apache-iceberg-1.12.0.tar.gz
  589  ls
  590  cd apache-iceberg-1.12.0
  591  ls
  592  ls -l gradlew
  593  java -version
  594  df -h .
  595  docker system df


  603  java -version
  604  apt install openjdk-21-jre-headless
  605  java -version
  606  javac -version
  607  java -version
  608  javac -version
  609  apt install -y openjdk-21-jdk-headless
  610  javac -version
  611  ./gradlew -x test -x integrationTest   :iceberg-kafka-connect:iceberg-kafka-connect-runtime:distZip
  612  df -h
  613  free -h
  614  dmesg -T | grep -iE 'killed process|out of memory|oom' | tail -20
  615  ./gradlew   --no-daemon   --max-workers=1   -Dorg.gradle.parallel=false   -Dorg.gradle.jvmargs="-Xmx1024m -XX:MaxMetaspaceSize=512m -Dfile.encoding=UTF-8"   -x test   -x integrationTest   :iceberg-kafka-connect:iceberg-kafka-connect-runtime:distZip
  616  ls -lh kafka-connect/kafka-connect-runtime/build/distributions/
  617  unzip -l kafka-connect/kafka-connect-runtime/build/distributions/*.zip | head -60
  618  apt install unzip
  619  unzip -l kafka-connect/kafka-connect-runtime/build/distributions/*.zip | head -60
  620  mkdir -p /root/data-platform/phase3/connect/plugins
  621  unzip -q   kafka-connect/kafka-connect-runtime/build/distributions/iceberg-kafka-connect-runtime-1.12.0.zip   -d /root/data-platform/phase3/connect/plugins
  622  du -sh /root/data-platform/phase3/connect/plugins/iceberg-kafka-connect-runtime-1.12.0
  623  ls -lh /root/data-platform/phase3/connect/plugins/iceberg-kafka-connect-runtime-1.12.0/lib/iceberg-kafka-connect*.jar
  624  cat /root/data-platform/phase3/connect/plugins/iceberg-kafka-connect-runtime-1.12.0/manifest.json
  625  history  | grep /opt/kafka/bin/kafka-topics.sh
  626  cd /root/data-platform/phase3
  627  docker compose exec kafka /opt/kafka/bin/kafka-topics.sh   --bootstrap-server kafka:9092   --create   --topic connect-configs   --partitions 1   --replication-factor 1   --config cleanup.policy=compact
  628  docker compose exec kafka /opt/kafka/bin/kafka-topics.sh   --bootstrap-server kafka:9092   --create   --topic connect-offsets   --partitions 1   --replication-factor 1   --config cleanup.policy=compact
  629  docker compose exec kafka /opt/kafka/bin/kafka-topics.sh   --bootstrap-server kafka:9092   --create   --topic connect-status   --partitions 1   --replication-factor 1   --config cleanup.policy=compact
  630  docker compose exec kafka /opt/kafka/bin/kafka-topics.sh   --bootstrap-server kafka:9092   --list
  631  docker run --rm apache/kafka:4.1.1   /opt/kafka/bin/connect-distributed.sh --version
  632  ls -ld /root/data-platform/phase3/connect/plugins/iceberg-kafka-connect-runtime-1.12.0
  633  free -h
  634  mkdir -p connect/config
  635  cat > connect/config/worker.properties <<'EOF'
  636  bootstrap.servers=kafka:9092
  637  group.id=iceberg-connect-cluster
  638  key.converter=org.apache.kafka.connect.storage.StringConverter
  639  value.converter=org.apache.kafka.connect.json.JsonConverter
  640  value.converter.schemas.enable=false
  641  config.storage.topic=connect-configs
  642  config.storage.replication.factor=1
  643  offset.storage.topic=connect-offsets
  644  offset.storage.replication.factor=1
  645  offset.storage.partitions=1
  646  status.storage.topic=connect-status
  647  status.storage.replication.factor=1
  648  status.storage.partitions=1
  649  plugin.path=/opt/kafka/plugins
  650  rest.host.name=0.0.0.0
  651  rest.port=8083
  652  offset.flush.interval.ms=10000
  653  EOF
  654  cat connect/config/worker.properties
  655  docker image inspect apache/kafka:4.1.1   --format 'Image: {{.RepoTags}}'
  656  vi docker-compose.yml
  657  docker compose config -q
  658  docker compose config | sed -n '/kafka-connect:/,/^[^ ]/p'
  659  docker compose up -d kafka-connect
  660  docker compose ps kafka-connect
  661  docker compose logs --tail=100 kafka-connect
  662  curl -i http://localhost:8083/
  663  curl -s http://localhost:8083/connector-plugins
  664  curl -s http://localhost:8083/connector-plugins | jq .
  665  curl -s -X PUT   -H "Content-Type: application/json"   http://localhost:8083/connector-plugins/org.apache.iceberg.connect.IcebergSinkConnector/config/validate
  666  curl --include   --aws-sigv4 'aws:amz:us-east-1:s3'   --user 'admin:secret'   'http://localhost:8181/v1/iceberg-warehouse/namespaces'
  667  docker compose exec kafka   /opt/kafka/bin/kafka-topics.sh   --bootstrap-server localhost:9092   --create   --topic control-iceberg   --partitions 1   --replication-factor 1
  668  docker compose exec kafka   /opt/kafka/bin/kafka-topics.sh   --bootstrap-server localhost:9092   --describe   --topic control-iceberg
  669  curl --include   --aws-sigv4 'aws:amz:us-east-1:s3'   --user 'admin:secret'   'http://localhost:8181/v1/iceberg-warehouse/config'
  670  curl --include   'http://localhost:8181/v1/config'
  671  docker run --rm   --network phase3_default   -e AWS_ACCESS_KEY_ID=admin   -e AWS_SECRET_ACCESS_KEY=secret   -e AWS_DEFAULT_REGION=us-east-1   amazon/aws-cli:latest   --endpoint-url http://seaweedfs:8333   s3api head-bucket   --bucket iceberg-warehouse
