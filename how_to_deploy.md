Привет!

Инструкция по развертыванию проекта. 
В качестве примера использовалась ВМ с YandexCloud с ОС Ubuntu-24.

1) Допустим, что машина запущена и мы к ней подключились в терминале через ssh.

2) Клонируйте репозиторий и перейдите в него
```
git clone https://github.com/NikitaKuzlyaev/GridArena
cd GridArena
```

3) Теперь поработаем с конфигурацией.
   * Перейдите в *backend/configuration/settings.py* и убедитесь, что тип установлена среда "DEVELOPMENT":
    
   ```current_environment = Environment.DEVELOPMENT```

    * Проверьте *backend/configuration/.env.development* и убедитесь, что он вас устраивает. 
   По желанию вы можете менять любые параметры и ключи.
    * Откройте *frontend/react/src/config.js* и укажите реальный адрес на котором расположен backend. 
   В текущей реализации frontend и backend на одном сервере и адресе, например, если публичный ip адрес машины *158.160.135.116*, то
   укажите ```'http://158.160.135.116:80/'``` (у вас может быть другой порт и протокол!)


4) Обновление linux и установка необходимых пакетов.

* Обновляем систему
```
sudo apt update && sudo apt upgrade -y
```

* Устанавливаем зависимости
```
sudo apt install -y ca-certificates curl gnupg lsb-release
```

* Нужно добавить официальный GPG-ключ Docker
```
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
```

* И добавить репозиторий Docker
```
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
 ```

* И установить Docker Engine и зависимости
```
sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

* (Опционально) Можно установить legacy - если ваш проект использует docker-compose (а не docker compose)
```
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

* Запускаем Docker и включаем автозапуск
```
sudo systemctl start docker
sudo systemctl enable docker
```

* Добавляем текущего пользователя в группу docker
```
sudo usermod -aG docker $USER
```

5) Запустите спорку контейнера с базой данных

```
sudo docker-compose up --build -d postgres
```

6) Нам необходимы некоторые пакеты python для настройки, поэтому выполните следующие команды:

```
sudo apt install python3.12-venv
python3 -m venv venv
source venv/bin/activate
pip install pydantic-settings alembic psycopg2-binary asyncpg
sudo apt install libpq-dev python3-dev
```

7) Затем выполните инструкции по инициализации базы данных из *backend/setup/readme.md*

8) Теперь мы готовы выполнить build всего проекта. Выполните команду, находясь в директории *GridArena*:
```
sudo docker-compose up --build
```

9) Готово! Проект запущен по ващему адресу - перейдите на *http://{your_ip}:80/*