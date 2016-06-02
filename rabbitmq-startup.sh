#!/bin/sh
cat <<EOF > /etc/apt/sources.list.d/rabbitmq.list
deb http://www.rabbitmq.com/debian/ testing main
EOF

curl https://www.rabbitmq.com/rabbitmq-release-signing-key.asc -o /tmp/rabbitmq-release-signing-key.asc
apt-key add /tmp/rabbitmq-release-signing-key.asc
rm /tmp/rabbitmq-release-signing-key.asc

apt-get -qy update
apt-get -qy install rabbitmq-server

rabbitmqctl add_user test test
rabbitmqctl set_user_tags test administrator
rabbitmqctl set_permissions -p / test ".*" ".*" ".*"

rabbitmq-plugins enable rabbitmq_management