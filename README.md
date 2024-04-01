### Парсер товара fix-price

*  Парсер данных товара определённой категории


### Как запустить проект:

* Клонировать репозиторий:

    ```
    git@github.com:Evgenmater/fixprice_scrapy.git
    ```

* Перейти в директорию проекта:

    ```
    cd fixprice_scrapy
    ```

* Создайте и активируйте виртуальное окружение, обновите менеджер пакетов pip и установите зависимости из файла requirements.txt:

    ```
    python -m venv venv
    source venv/Scripts/activate
    python -m pip install --upgrade pip
    pip install -r requirements.txt 
    ```

* Команда для работы с парсингом:

    ```
    scrapy crawl fixprice
    ```

### Автор:  
Хлебнев Евгений Юрьевич<br>
**email**: hlebnev@yandex.ru<br>
**telegram** @Evgen0991