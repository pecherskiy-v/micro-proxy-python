#!/bin/bash

# Определяем дистрибутив
. /etc/os-release

# Путь к текущему скрипту
SCRIPT_DIR=$(dirname $(readlink -f $0))

# Устанавливаем зависимости
if [[ "$ID" == "ubuntu" ]]; then
    sudo apt-get update
    sudo apt-get install -y certbot python3-pip
    INIT_SYSTEM="systemd"
elif [[ "$ID" == "alpine" ]]; then
    apk add --no-cache certbot py3-pip
    INIT_SYSTEM="openrc"
else
    echo "Only Ubuntu and Alpine are supported"
    exit 1
fi

# Устанавливаем Python зависимости
pip3 install Flask requests

# Читаем переменные окружения из ini файла
export $(awk -F "=" '{print $1"="$2}' config.ini)

# Получаем сертификат
sudo certbot certonly --standalone -d $YOUR_DOMAIN --register-unsafely-without-email --agree-tos

# Добавляем cron для обновления сертификата
(crontab -l ; echo "0 3 * * * /usr/bin/certbot renew --quiet") | crontab -

# Генерируем файлы сервисов
if [[ "$INIT_SYSTEM" == "systemd" ]]; then
    cat <<EOL > /etc/systemd/system/proxy.service
    [Unit]
    Description=My Proxy Service
    After=network.target

    [Service]
    ExecStart=/usr/bin/python3 $SCRIPT_DIR/main.py
    Restart=always
    User=nobody
    RestartSec=3
    LimitNOFILE=4096

    [Install]
    WantedBy=multi-user.target
EOL

    sudo systemctl enable /etc/systemd/system/proxy.service
    sudo systemctl start proxy.service

elif [[ "$INIT_SYSTEM" == "openrc" ]]; then
    cat <<EOL > /etc/init.d/proxy
    #!/sbin/openrc-run

    description="My Proxy Service"
    command="/usr/bin/python3"
    command_args="$SCRIPT_DIR/main.py"
    command_background="true"
    pidfile="/var/run/proxy.pid"
    start_stop_daemon_args="--background --make-pidfile"

    depend() {
        need net
        after firewall
    }
EOL

    sudo chmod +x /etc/init.d/proxy
    sudo rc-update add proxy default
    sudo rc-service proxy start
fi
