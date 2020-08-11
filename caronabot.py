from selenium import webdriver
import time
from bs4 import BeautifulSoup
import requests
import tweepy
# Authenticate to Twitter
# f = open('keys.txt')
# for i in range(4):
# 	print(f.readline())
auth = tweepy.OAuthHandler(keys)
auth.set_access_token(keys)
class Twitter(): ### Login num API só pra pegar msgs da lamsa
    def __init__(self):
        auth = tweepy.OAuthHandler(keys)
        auth.set_access_token(keys)
        self.api = tweepy.API(auth)

    def read_tweet(self, sentido):  ##Sentido refere ao sentido da linha amarela
        tweets = self.api.user_timeline(id='LinhaAmarelaRJ', count=5, include_rts=False)
        for status in tweets:
            tweet_clean = status._json['text']
            tweet_clean = tweet_clean.split('-')
            tweet_clean[1] = ' '.join(tweet_clean[1].replace('#LamsaInforma', '').split())
            word_check = tweet_clean[1].split()
            hour = tweet_clean[0].strip()
            if 'sentidos' in word_check:
                return f'{tweet_clean[1]} (Última atualização às {tweet_clean[0]})' 
            elif sentido in word_check:  
                return f'*CaronaBot*: {tweet_clean[1]} (Última atualização às {tweet_clean[0][:-1]})' 

class WhatsappBot():
    def __init__(self):
        # Altere o nome dos grupos aqui
        options = webdriver.ChromeOptions()
        options.add_argument('lang=pt-br')
        self.driver = webdriver.Chrome(executable_path=r'./chromedriver.exe')
        self.driver.get('https://web.whatsapp.com')
        time.sleep(10)
        print('ready to start!')       
        self.grupo = self.driver.find_element_by_xpath(f"//span[@title='bot test']")

    def grupo_click(self): #Abrir o grupo
        try:
            self.grupo.click()
        except:
            pass

    def send_message(self, mensagem):
        chat_box = self.driver.find_element_by_class_name("_3uMse")
        chat_box.click()
        chat_box.send_keys(mensagem)
        botao_enviar = self.driver.find_element_by_xpath("//span[@data-icon='send']")
        botao_enviar.click()

    def driver_quit(self):
        self.driver.quit()
        return 'quit successfully!'

    def read_message(self):
        soup = BeautifulSoup(self.driver.page_source, "html.parser")
        msg_whats = soup.find_all(True, {'class': "_3Whw5 selectable-text invisible-space copyable-text"})[-1].get_text()

        #.get_text()
        #["FTBzM message-in", "FTBzM _4jEk2 message-in"]
        return msg_whats

#-----------------------------------------------------beginning of code itself-------------------------------------------------#       

bot = WhatsappBot()
x = input('enter to read group')
bot.grupo_click()
msg_list_fundao = [
 '@bot fundão',
 '@Bot fundão',
 '@Bot Fundão',
 '@bot Fundão',
 '@bot fundao',
 '@Bot fundao',
 '@Bot Fundao',
 '@bot Fundao'
]
msg_list_barra = [
'@bot barra',
'@bot Barra',
'@Bot barra',
'@Bot Barra',
]
# while x != 'stop':
while True:
    msg_whats = bot.read_message()
    if msg_whats in msg_list_fundao:
        sentido = 'Fundão'
        print('comando fundão reconhecido!')
        lamsa = Twitter()
        tweet = lamsa.read_tweet(sentido)
        bot.send_message(tweet)
    elif msg_whats in msg_list_barra:
        sentido = 'Barra'
        print('comando barra reconhecido')
        lamsa = Twitter()
        tweet = lamsa.read_tweet(sentido)
        bot.send_message(tweet)
    time.sleep(10)

print('Leaving script!')
bot.driver_quit()





