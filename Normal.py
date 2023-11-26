import requests
import bs4
import json

# Укажите URL страницы с товарами
url = "https://www.auchan.ru/catalog/ovoschi-frukty-zelen-griby-yagody/"

# Получите ответ от сервера
response = requests.get(url)

# Создайте объект BeautifulSoup для обработки HTML-кода
soup = bs4.BeautifulSoup(response.content, "lxml")

# Найдите все элементы товара
products = soup.find_all("h1", class_="active css-144arr9")

# Создайте пустой список для хранения товаров
products_data = []

# Цикл по всем товарам
for product in products:
    # Получите ID товара
    id = product["ProductName"]

    # Получите наименование товара
    name = product.find("h1", class_="css-1dud7uh").text

    # Получите ссылку на товар
    link = product.find("a", class_="rr-item__info rr-item__title")["href"]

    # Получите регулярную цену товара
    regular_price = product.find("div", class_="oldPricePDP css-ok3jdb").text

    # Получите промо цену товара
    promo_price = product.find("div", class_="fullPricePDP css-5ig8q6").text

    # Получите бренд товара
    brand = product.find("td", class_="css-1v23ygr").text

    # Проверяем, есть ли товар в наличии
    in_stock = (
        product.find("span", class_="inStockData css-17mx28f").text == "В наличии"
    )

    # Если товар в наличии, добавляем его в список
    if in_stock:
        products_data.append(
            {
                "id": id,
                "name": name,
                "link": link,
                "regular_price": regular_price,
                "promo_price": promo_price,
                "brand": brand,
            }
        )

# Сохраните данные в JSON-файл
with open("products.json", "w") as f:
    json.dump(products_data, f)
