import EzTG
import requests
import json
import pandas as pd
import csv
import gender_guesser.detector as gender

def callback(bot, update):
    # here's your bot
    if 'message' in update:
        # messages "handler"
        message_id = update['message']['message_id']  # https://core.telegram.org/bots/api#message
        user_id = update['message']['from']['id']
        chat_id = update['message']['chat']['id']
        text = update['message']['text']

        if text == '/start':
            keyboard = EzTG.Keyboard('inline')
            keyboard.add('Nominativi', 'callback data')
            keyboard.newLine()
            keyboard.add('Numeri di telefono', 'callback data 2')
            keyboard.newLine()
            keyboard.add('Indirizzi e-mail', 'callback data 3')
            keyboard.newLine()
            keyboard.add('Contatori', 'callback data 4')
            keyboard.newLine()
            keyboard.add('CSV per Nome', 'callback data 5')
            keyboard.newLine()
            keyboard.add('CSV per Orario prenotazione', 'callback data 6')
            bot.sendMessage(chat_id=chat_id, text='Ciao sono il Bot per gli eventi del Macro!\nScegli uno dei seguenti comandi:\n', reply_markup=keyboard)  # you can find method parameters in https://core.telegram.org/bots/api#sendmessage

        if text == '/keyboard':
            keyboard = EzTG.Keyboard('keyboard')
            keyboard.add('Example 1')
            keyboard.add('Example 2')
            keyboard.newLine()
            keyboard.add('Example 3')
            bot.sendMessage(chat_id=chat_id, text='Test',
                            reply_markup=keyboard)

        if text == '/hidekb':
            keyboard = EzTG.Keyboard('remove')
            bot.sendMessage(chat_id=chat_id,
                            text='Adios keyboard', reply_markup=keyboard)
    if 'callback_query' in update:
        # callback query "handler"
        message_id = update['callback_query']['message']['message_id']
        user_id = update['callback_query']['from']['id']
        chat_id = update['callback_query']['message']['chat']['id']
        cb_id = update['callback_query']['id']
        cb_data = update['callback_query']['data']
        r = requests.get("https://macro-api.herokuapp.com/clients").json()

        if cb_data == 'callback data':
            keyboard = EzTG.Keyboard('inline')
            keyboard.add('Numeri di telefono', 'callback data 2')
            keyboard.newLine()
            keyboard.add('Indirizzi e-mail', 'callback data 3')
            keyboard.newLine()
            keyboard.add('Contatori', 'callback data 4')
            keyboard.newLine()
            keyboard.add('CSV per Nome', 'callback data 5')
            keyboard.newLine()
            keyboard.add('CSV per Orario prenotazione', 'callback data 6')
            l = sorted([x['nomeCompleto'] for x in r])
            s = '\n'.join(l)
            bot.editMessageText(chat_id=chat_id, message_id=message_id, reply_markup=keyboard,
                                text='[Lista Prenotati]\n\n' + s + '\n\nTotale: ' + str(len(l)) + ' prenotati\n')  # you can find method parameters in https://core.telegram.org/bots/api#editmessagetext

        if cb_data == 'callback data 2':
            keyboard = EzTG.Keyboard('inline')
            keyboard.add('Nominativi', 'callback data')
            keyboard.newLine()
            keyboard.add('Indirizzi e-mail', 'callback data 3')
            keyboard.newLine()
            keyboard.add('Contatori', 'callback data 4')
            keyboard.newLine()
            keyboard.add('CSV per Nome', 'callback data 5')
            keyboard.newLine()
            keyboard.add('CSV per Orario prenotazione', 'callback data 6')
            l = sorted([x['nomeCompleto'] + '\n\t' + str(x['cell']) for x in r])
            s = '\n'.join(l)
            bot.editMessageText(chat_id=chat_id, message_id=message_id, reply_markup=keyboard,
                                text='[Lista Prenotati con Cellulare]\n\n' + s) 
        
        if cb_data == 'callback data 3':
            keyboard = EzTG.Keyboard('inline')
            keyboard.add('Nominativi', 'callback data')
            keyboard.newLine()
            keyboard.add('Numeri di telefono', 'callback data 2')
            keyboard.newLine()
            keyboard.add('Contatori', 'callback data 4')
            keyboard.newLine()
            keyboard.add('CSV per Nome', 'callback data 5')
            keyboard.newLine()
            keyboard.add('CSV per Orario prenotazione', 'callback data 6')
            l = sorted([x['nomeCompleto'] + '\n\t' + x['email'] for x in r])
            s = '\n'.join(l)
            bot.editMessageText(chat_id=chat_id, message_id=message_id, reply_markup=keyboard,
                                text='[Lista Prenotati con Email]\n\n' + s)
        if cb_data == 'callback data 4':
            keyboard = EzTG.Keyboard('inline')
            keyboard.add('Nominativi', 'callback data')
            keyboard.newLine()
            keyboard.add('Numeri di telefono', 'callback data 2')
            keyboard.newLine()
            keyboard.add('Indirizzi e-mail', 'callback data 3')
            keyboard.newLine()
            keyboard.add('CSV per Nome', 'callback data 5')
            keyboard.newLine()
            keyboard.add('CSV per Orario prenotazione', 'callback data 6')
            total = len(r)
            d = gender.Detector(case_sensitive=False)
            male = 0
            female = 0
            nomi = [ (x['nomeCompleto'].split(' ')[0] , d.get_gender(x['nomeCompleto'].split(' ')[0])) for x in r]
            maleBug = ["Nicola", "Simone","Daniele", "Michele", "Gabriele"]
            for n in nomi:
                key = n[0]
                value = n[1]
                print(key + " : " + value + "\n")
                if (value == 'male' or value == 'mostly_male' or key in maleBug):
                    male += 1
                elif (value == 'female' or value == 'mostly_female'):
                    female += 1
            bot.editMessageText(chat_id=chat_id, message_id=message_id, reply_markup=keyboard, text='[Contatori]\n\n' + "Prenotati: " + str(total) + "\n\n" + "[ Bregnometro ]\n Tanta?\n" + "Male: " + str(male) + "\n" + "Female: " + str(female) + "\n" + "Unknown: " + str((total - male - female)))

        if cb_data == 'callback data 5':
            keyboard = EzTG.Keyboard('inline')
            keyboard.add('Nominativi', 'callback data')
            keyboard.newLine()
            keyboard.add('Numeri di telefono', 'callback data 2')
            keyboard.newLine()
            keyboard.add('Indirizzi e-mail', 'callback data 3')
            keyboard.newLine()
            keyboard.add('Contatori', 'callback data 4')
            keyboard.newLine()
            keyboard.add('CSV per Orario prenotazione', 'callback data 6')
            req = requests.get("https://macro-api.herokuapp.com/clients-filtered").json()
            ls = sorted(req, key = lambda x : x["nomeCompleto"])
            keys = ls[0].keys()
            with open('Prenotazioni.csv', 'w+', newline='')  as output_file:
                dict_writer = csv.DictWriter(output_file, keys)
                dict_writer.writeheader()
                dict_writer.writerows(ls)
            output_file.close()
            files = {'document' : open("Prenotazioni.csv", "rb")}
            requests.post("https://api.telegram.org/bot1760533457:AAEH_JJs6ufGtqZilm1eRSKPmxy1eito-iE/sendDocument?chat_id=" + str(chat_id), files=files)
            bot.editMessageText(chat_id=chat_id, message_id=message_id, reply_markup=keyboard, text='[ Download CSV ]')

        if cb_data == 'callback data 6':
            keyboard = EzTG.Keyboard('inline')
            keyboard.add('Nominativi', 'callback data')
            keyboard.newLine()
            keyboard.add('Numeri di telefono', 'callback data 2')
            keyboard.newLine()
            keyboard.add('Indirizzi e-mail', 'callback data 3')
            keyboard.newLine()
            keyboard.add('Contatori', 'callback data 4')
            keyboard.newLine()
            keyboard.add('CSV per Nome', 'callback data 5')
            req = requests.get("https://macro-api.herokuapp.com/clients-filtered").json()
            keys = req[0].keys()
            with open('Prenotazioni.csv', 'w+', newline='')  as output_file:
                dict_writer = csv.DictWriter(output_file, keys)
                dict_writer.writeheader()
                dict_writer.writerows(req)
            output_file.close()
            files = {'document' : open("Prenotazioni.csv", "rb")}
            requests.post("https://api.telegram.org/bot1760533457:AAEH_JJs6ufGtqZilm1eRSKPmxy1eito-iE/sendDocument?chat_id=" + str(chat_id), files=files)
            bot.editMessageText(chat_id=chat_id, message_id=message_id, reply_markup=keyboard, text='[ Download CSV ]')


bot = EzTG.EzTG(token='1760533457:AAEH_JJs6ufGtqZilm1eRSKPmxy1eito-iE',
                callback=callback)
