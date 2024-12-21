# CW_var19

Для корректной работы желательно установить Python 3.10.x (рекомендуется .11).
Если запускать backend на Ubuntu, то заранее обновите все пакеты через терминал:

```bash
sudo apt-get update && sudo apt-get upgrade
Шаги установки
Скачайте архив с курсовой работой в отдельную папку и распакуйте его.

Откройте папку с распакованным архивом в VS Code.

Установка виртуальной среды venv:

Откройте терминал в VS Code и введите:
bash
Копировать код
python3 -m venv venv
(для всех ОС)
Для активации виртуальной среды:
Windows:
bash
Копировать код
venv\Scripts\activate.bat
Linux (Ubuntu):
bash
Копировать код
source venv/bin/activate
Если все шаги выполнены верно, после активации виртуальной среды появится приписка (venv) в терминале VS Code.
Установите необходимые пакеты для работы backend:
bash
Копировать код
pip install fastapi motor pydantic uvicorn jinja2 aiofiles python-multipart
Для деактивации виртуальной среды введите:
bash
Копировать код
deactivate
Установка Docker на виртуальной машине с Ubuntu (если Docker еще не установлен):

Добавьте официальный GPG-ключ Docker:
bash
Копировать код
sudo apt-get update
sudo apt-get install ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc
Добавьте репозиторий Docker в источники APT:
bash
Копировать код
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update
Установите Docker:
bash
Копировать код
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
Для проверки установки Docker введите:
bash
Копировать код
sudo docker run hello-world
Если все установлено правильно, будет выведено сообщение от Docker.
Запуск NoSQL базы данных MongoDB на Docker:

Запустите команду для загрузки MongoDB:
bash
Копировать код
sudo docker pull mongo
Запустите контейнер MongoDB:
bash
Копировать код
sudo docker run --name mongo_db -p 27017:27017 -d mongo
Проверка работы MongoDB:

Установите MongoDB Shell:
bash
Копировать код
sudo apt install mongodb-mongosh
Запустите MongoDB Shell:
bash
Копировать код
mongosh
Это позволит вам просматривать содержимое базы данных в терминальном интерфейсе Mongo.
Настройка подключения к базе данных в main.py:

Если вы используете Windows и Ubuntu, укажите IP-адрес виртуальной машины:
python
Копировать код
client = AsyncIOMotorClient("mongodb://адрес_виртуальной_машины:27017/")
Если все работает на Ubuntu, используйте:
python
Копировать код
client = AsyncIOMotorClient("mongodb://localhost:27017/")
Или:
python
Копировать код
client = AsyncIOMotorClient("mongodb://адрес_виртуальной_машины:27017/")
Запуск приложения: Если все шаги выполнены верно, откройте браузер и перейдите по адресу:

arduino
Копировать код
http://127.0.0.1:8000/students/form
Вы увидите HTML-форму для работы с базой данных.
