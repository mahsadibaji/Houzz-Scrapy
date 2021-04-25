# Houzz-Scrapy
crawl [houzz](https://www.houzz.com/) data with python scrapy.

# Set Up and Run
1.   clone this repository using git `clone https://github.com/mahsadibaji/Houzz-Scrapy.git`
2.   create and activate virtual environment 
1.   install requirements using `pip3 install -r requirements.txt`
2.   run project to crawl `category_name` until `page_number` using `scrapy crawl houzz –o filename.csv –a category=category_name –a to_page=page_number`
