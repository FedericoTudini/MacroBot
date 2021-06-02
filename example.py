import EzTG
import requests
import json

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
            keyboard.add('Lista prenotati', 'callback data')
            keyboard.newLine()
            keyboard.add('Numeri di telefono', 'callback data 2')
            keyboard.newLine()
            keyboard.add('Indirizzi e-mail', 'callback data 3')
            keyboard.newLine()
            keyboard.add('Contatori', 'callback data 4')
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
        r = requests.get("http://3.143.236.50:3000/clients").json()

        if cb_data == 'callback data':
            #bot.answerCallbackQuery(callback_query_id=cb_id, text='example #1')  # you can find method parameters in https://core.telegram.org/bots/api#answercallbackquery
            #keyboard = EzTG.Keyboard('inline')
            #keyboard.add('Example 2', 'callback data 2')
            l = sorted([x['nomeCompleto'] for x in r])
            s = '\n'.join(l)
            bot.editMessageText(chat_id=chat_id, message_id=message_id,
                                text='[Lista Prenotati]\n\n' + s + '\n\nTotale: ' + str(len(l)) + ' prenotati\n')  # you can find method parameters in https://core.telegram.org/bots/api#editmessagetext
            keyboard = EzTG.Keyboard('inline')
            keyboard.add('Lista prenotati', 'callback data')
            keyboard.newLine()
            keyboard.add('Numeri di telefono', 'callback data 2')
            keyboard.newLine()
            keyboard.add('Indirizzi e-mail', 'callback data 3')
            keyboard.newLine()
            keyboard.add('Contatori', 'callback data 4')

        if cb_data == 'callback data 2':
            l = sorted([x['nomeCompleto'] + '\n\t' + str(x['cell']) for x in r])
            s = '\n'.join(l)
            bot.editMessageText(chat_id=chat_id, message_id=message_id,
                                text='[Lista Prenotati con Cellulare]\n\n' + s)
            keyboard = EzTG.Keyboard('inline')
            keyboard.add('Lista prenotati', 'callback data')
            keyboard.newLine()
            keyboard.add('Numeri di telefono', 'callback data 2')
            keyboard.newLine()
            keyboard.add('Indirizzi e-mail', 'callback data 3')
            keyboard.newLine()
            keyboard.add('Contatori', 'callback data 4')
        
        if cb_data == 'callback data 3':
            l = sorted([x['nomeCompleto'] + '\n\t' + str(x['email']) for x in r])
            s = '\n'.join(l)
            bot.editMessageText(chat_id=chat_id, message_id=message_id,
                                text='[Lista Prenotati con Email]\n\n' + s)
            keyboard.add('Lista prenotati', 'callback data')
            keyboard.newLine()
            keyboard.add('Numeri di telefono', 'callback data 2')
            keyboard.newLine()
            keyboard.add('Indirizzi e-mail', 'callback data 3')
            keyboard.newLine()
            keyboard.add('Contatori', 'callback data 4')

        if cb_data == 'callback data 4':
            total = len(r)
            bot.editMessageText(chat_id=chat_id, message_id=message_id, text='[Contatori]\n\n' + "Prenotati:" + str(total) + "\n")
            keyboard.add('Lista prenotati', 'callback data')
            keyboard.newLine()
            keyboard.add('Numeri di telefono', 'callback data 2')
            keyboard.newLine()
            keyboard.add('Indirizzi e-mail', 'callback data 3')
            keyboard.newLine()
            keyboard.add('Contatori', 'callback data 4')


bot = EzTG.EzTG(token='1760533457:AAEH_JJs6ufGtqZilm1eRSKPmxy1eito-iE',
                callback=callback)
