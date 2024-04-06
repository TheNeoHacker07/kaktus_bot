import telebot
import requests
from bs4 import BeautifulSoup



bot=telebot.TeleBot('6434983720:AAETx5Mj3oiUX7aBUn9TxeeRG4VQVFaDwvo')

date=None

@bot.message_handler(commands=['start'])
def start_func_message(message):
    bot.send_message(message.chat.id,"hello")


@bot.message_handler(commands=['news'])
def news_func(message):
    global date
    bot.send_message(message.chat.id, 'Введите дату для новостей')


@bot.message_handler(func=lambda message: True)
def fetch_news(message):
    global date  
    date = message.text.strip()
 


    url_data=f'https://kaktus.media/?lable=8&date={date}&order=time'
    def get_url(URL):
        response=requests.get(URL).text
        return response

    response_data=get_url(url_data)

    def get_HTML(response):
        soup=BeautifulSoup(response,"lxml")
        news=soup.find_all('div',class_="ArticleItem")
        return news

    html_data=get_HTML(response_data)


    def get_datas(new_list):
        arr=[]
        for news in new_list:
            arr.append(
                {
                    "Заголовок":news.find("a",class_="ArticleItem--name").text.strip(),
                    "Ссылка":news.find("a",class_="ArticleItem--image").get('href')    
                }
            )
        return arr

    formatted_info=get_datas(html_data)
    for el in formatted_info:
        for el2 in el.values():
            bot.send_message(message.chat.id,el2) 
    
bot.polling(none_stop=True)
