# CW_var19
Для корректной работы желательно установить Python 3.10.x (рекомендуется .11)
Если запуск backend производить на Ubuntu, то заранее обновить все пакеты через терминал: sudo apt-get update && sudo apt-get upgrade
1. Скачать архив с курсовой работой в отдельную папку и распаковать его.
2.  При помощи VS code открыть папку, в которой находится распакованный архив.
3. Установка виртуальной среды vevn:
    3.1. открыть терминал VS code и ввести: python3 -m venv venv (для всех ОС);
    3.2. venv\Scripts\activate.bat для WINDOWS (если backend запускать на версии VS code для Windows)
      или source venv/bin/activate для LINUX(Ubuntu) (если backend запускать на версии VS code для Linux)
    3.3. Если все шаги выполнены верно, то после активации виртуальной среды появится приписка (venv) в терминале VS code;
    3.4. Устанавливаем необходимые пакеты для работы backend:
        pip install fastapi motor pydantic uvicorn jinja2 aiofiles python-multipart
    3.5. Для деактивации виртуальной среды необходимо ввести(если необходимо из нее выйти):
        deactivate venv

4. Если на виртуальной машине с Ubuntu не установлен докер, то необходимо выполнить следующие команды:

     4.1. # Add Docker's official GPG key:
          sudo apt-get update
          sudo apt-get install ca-certificates curl
          sudo install -m 0755 -d /etc/apt/keyrings
          sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
          sudo chmod a+r /etc/apt/keyrings/docker.asc
    
          # Add the repository to Apt sources:
          echo \
            "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
            $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
            sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
          sudo apt-get update
   
     4.2. sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
     4.3. Для проверки, установился ли докер ввести: 
          sudo docker run hello-world
          Если все поставлось успешно, то будет выведено собщение от докера.

5. Для запуска NoSQL базы MONGODB на докере необходимо:
     5.1. Прописать sudo docker pull mongo
     5.2. sudo docker run --name mongo_db -p 27017:27017 -d mongo

6. Чтобы проверить запустилась ли БД, можно прописать в терминале:
    sudo apt install mongodb-mongosh
    mongosh
    это позвволит просматривать содержимое базы данных в терминальном интерфейсе mongo

7. Открыть папку с распакованным архивом из пункта 2), а файле main.py указать ip адрес к БД:
      7.1. Если С Window на Ubuntu, то:  client = AsyncIOMotorClient("mongodb://адрес_виртаульной машины:27017/")
      7.2. Если все на Ubuntu, то:       client = AsyncIOMotorClient("mongodb://localhost:27017/") или client = AsyncIOMotorClient("mongodb://адрес_виртаульной машины:27017/")

8. Если все шаги выполнены верно, то в браузере по адресу http://127.0.0.1:8000/students/form откроется html форма для работы с БД.
