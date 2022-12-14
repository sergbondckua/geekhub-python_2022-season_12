"""
Використовуючи Scrapy, написати скрипт, який буде приймати на вхід:
назву та ID категорії (у форматі назва/id/) із сайту https://rozetka.com.ua і
буде збирати всі товари із цієї категорії, збирати всі можливі дані
(бренд, категорія, модель, ціна, рейтинг тощо) і зберігати їх у CSV файл
(наприклад, якщо передана категорія mobile-phones/c80003/,
то файл буде називатися c80003_products.csv)
"""

from scrapy.crawler import CrawlerProcess

from rozetka_api.rozetka_api.spiders.rozetka import RozetkaSpider

def main():
    """Main function"""
    category = "aksessuari-dlya-ochkov-virtualnoy-realnosti/c4659246"
    id_category = category.split("/", maxsplit=1)[-1]

    process = CrawlerProcess(settings={
        "FEEDS": {
                f"{id_category}_products.csv": {  # CSV file
                    "format": "csv",
                    "header": True,
                    "encoding": "utf-8",
                    "indent": True,
                    "overwrite": True},
                f"{id_category}_products.json": {  # JSON file
                    "format": "json",
                    "encoding": "utf-8",
                    "escape": False,
                    "newline": "",
                    "ensure_ascii": False,
                    "indent": 4,
                    "overwrite": True},
            },
    })

    process.crawl(RozetkaSpider, category=category)
    process.start()



if __name__ == '__main__':
    main()
