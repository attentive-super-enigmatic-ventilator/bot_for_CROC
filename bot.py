import google
import os
import smtplib
import random
import vk_api
import vk
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api import VkUpload
import mimetypes
from email import encoders
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.audio import MIMEAudio
from email.mime.multipart import MIMEMultipart
from pprint import pprint
import glob
import urllib.request

service_access_key = open('C:/Users/user/Desktop/bot_silaedr/service.txt').read().splitlines()
session = vk.Session(access_token=service_access_key)
api1 = vk.API(session, v=5.101, scope='wall')
owner_id = open('C:/Users/user/Desktop/bot_silaedr/owner.txt').read().splitlines()
admins = {str(i) for i in open('C:/Users/user/Desktop/bot_silaedr/admins.txt').read().splitlines()}
loginpassword = open('C:/Users/user/Desktop/bot_silaedr/login, password.txt').read().splitlines()
pochta = open('C:/Users/user/Desktop/bot_silaedr/mail.txt').read().splitlines()
tokens = open('C:/Users/user/Desktop/bot_silaedr/secret.txt').read().splitlines()
vk_session = vk_api.VkApi(token=tokens[0])
vko = vk_session.get_api()
app = open('C:/Users/user/Desktop/bot_silaedr/app.txt').read().splitlines()
sessio = vk.AuthSession(scope='wall', app_id=app, user_login=loginpassword[0], user_password=loginpassword[1].encode('utf-8').strip())
api = vk.API(sessio, v=5.101)
contacts = []
vk_sessio = vk_api.VkApi(loginpassword[0], loginpassword[1], app_id=int(app[0]), scope='wall, photos')
vk_sessio.auth()
upload = VkUpload(vk_sessio)


def sendmail(text, files):
    mail = smtplib.SMTP('smtp.mail.ru', 587)
    print(mail.starttls())
    print(mail.login(pochta[0], pochta[1]))
    msg = MIMEMultipart()
    msg['From'] = pochta[0]
    msg['Subject'] = 'Новости Силаэдра'
    msg.attach(MIMEText(text, 'plain'))
    for filepath in files:
        filename = os.path.basename(filepath)

        if os.path.isfile(filepath):
            ctype, encoding = mimetypes.guess_type(filepath)
            if ctype is None or encoding is not None:
                ctype = 'application/octet-stream'
            maintype, subtype = ctype.split('/', 1)
            if maintype == 'text':
                with open(filepath) as fp:
                    file = MIMEText(fp.read(), _subtype=subtype)
                    fp.close()
            elif maintype == 'image':
                with open(filepath, 'rb') as fp:
                    file = MIMEImage(fp.read(), _subtype=subtype)
                    fp.close()
            elif maintype == 'audio':
                with open(filepath, 'rb') as fp:
                    file = MIMEAudio(fp.read(), _subtype=subtype)
                    fp.close()
            else:
                with open(filepath, 'rb') as fp:
                    file = MIMEBase(maintype, subtype)
                    file.set_payload(fp.read())
                    fp.close()
                encoders.encode_base64(file)
            file.add_header('Content-Disposition', 'attachment', filename=filename)
            msg.attach(file)
    print(contacts)
    # mail.send_message(msg, to_addrs=contacts)
    mail.quit()


# sendmail('тест', ['C:/Users/user/Desktop/bot_silaedr/secret.txt', 'C:/Users/user/Desktop/bot_silaedr/1.jpg'])
flag = False
base = VkKeyboard(one_time=True)
base.add_button('Отправить', color=VkKeyboardColor.POSITIVE)
base = base.get_keyboard()


def create_keyb1(buttons):
    keyboard = VkKeyboard(one_time=True)
    for b in buttons:
        if b == 'new_line':
            keyboard.add_line()
        else:
            keyboard.add_button(b, color=VkKeyboardColor.POSITIVE)
    keyboard = keyboard.get_keyboard()
    return keyboard


def create_keyb(buttons):
    keyboard = VkKeyboard(one_time=True)
    for b in buttons:
        if b == 'new_line':
            keyboard.add_line()
        else:
            keyboard.add_button(b, color=VkKeyboardColor.POSITIVE)
    keyboard.add_line()
    keyboard.add_button('Отменить отправку', color=VkKeyboardColor.NEGATIVE)
    keyboard = keyboard.get_keyboard()
    return keyboard


folder = 'C:/Users/user/Desktop/bot_silaedr/photos'
for the_file in os.listdir(folder):
    file_path = os.path.join(folder, the_file)
    try:
        if os.path.isfile(file_path):
            os.unlink(file_path)
        # elif os.path.isdir(file_path): shutil.rmtree(file_path)
    except Exception as e:
        print(e)

stop = VkKeyboard(one_time=True)
stop.add_button('Отменить отправку', color=VkKeyboardColor.NEGATIVE)
stop = stop.get_keyboard()

f_mail = False
f_group = False
news = ''
users = {}
# while True:
#    try:
print(1)
for event in VkLongPoll(vk_session).listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me and str(event.user_id) in admins:
        print(event.message_id)
        if event.user_id not in users:
            users[event.user_id] = 0
        bred = True
        inf = (vko.users.get(user_ids=event.user_id)[0])
        print('Я получил сообщение от '+(inf['first_name']) + ' ' +
              inf['last_name'])
        text = event.text.lower()
        pprint(event.attachments)
        # vko.photos.getById(photos=event.attachments['attach1'])
        if text == 'отменить отправку':
            vko.messages.send(user_id=event.user_id,
                              random_id=random.randint(1, 10 ** 9),
                              message='Отправка отменена! Обращайтесь, когда появятся новости!', keyboard=base)
            news = ''
            bred = False
            f_group = False
            f_mail = False
            users[event.user_id] = 0
            contacts = []
            folder = 'C:/Users/user/Desktop/bot_silaedr/photos'
            for the_file in os.listdir(folder):
                file_path = os.path.join(folder, the_file)
                try:
                    if os.path.isfile(file_path):
                        os.unlink(file_path)
                    # elif os.path.isdir(file_path): shutil.rmtree(file_path)
                except Exception as e:
                    print(e)
            continue
        if text == 'нет, спасибо':
            f_group = False
            f_mail = False
            vko.messages.send(user_id=event.user_id,
                              random_id=random.randint(1, 10 ** 9),
                              message='Хорошо! Обращайтесь, когда появятся еще новости!',
                              keyboard=base)
            users[event.user_id] = 0
            if contacts != []:
                print(contacts)
                sendmail(news, glob.glob("C:/Users/user/Desktop/bot_silaedr/photos/*.jpg"))
            contacts = []
            news = ''
            bred = False
            folder = 'C:/Users/user/Desktop/bot_silaedr/photos'
            for the_file in os.listdir(folder):
                file_path = os.path.join(folder, the_file)
                try:
                    if os.path.isfile(file_path):
                        os.unlink(file_path)
                    # elif os.path.isdir(file_path): shutil.rmtree(file_path)
                except Exception as e:
                    print(e)
        if text == 'отправить ранее выбранным контактам' or text == 'отправить новость':
            if not f_group:
                vko.messages.send(user_id=event.user_id,
                                  random_id=random.randint(1, 10 ** 9),
                                  message='Новость отправлена на почту выбранным контактам! Вы хотите отправить новость еще куда-нибудь?',
                                  keyboard=create_keyb1(['Группа ВК', 'new_line', 'Нет, спасибо']))
                f_mail = True
                users[event.user_id] = 2
                if contacts != []:
                    print(contacts)
                    sendmail(news, glob.glob("C:/Users/user/Desktop/bot_silaedr/photos/*.jpg"))
            else:
                f_group = False
                f_mail = False
                vko.messages.send(user_id=event.user_id,
                                  random_id=random.randint(1, 10 ** 9),
                                  message='Новость отправлена на почту выбранным контактам! Обращайтесь, когда появятся еще новости!',
                                  keyboard=base)
                users[event.user_id] = 0
                if contacts != []:
                    print(contacts)
                    sendmail(news, glob.glob("C:/Users/user/Desktop/bot_silaedr/photos/*.jpg"))
                contacts = []
                news = ''
                bred = False
                folder = 'C:/Users/user/Desktop/bot_silaedr/photos'
                for the_file in os.listdir(folder):
                    file_path = os.path.join(folder, the_file)
                    try:
                        if os.path.isfile(file_path):
                            os.unlink(file_path)
                        # elif os.path.isdir(file_path): shutil.rmtree(file_path)
                    except Exception as e:
                        print(e)
            bred = False
        if users[event.user_id] == 1:
            news = event.text
            flag = False
            photos = api1.messages.getById(message_ids=event.message_id, group_id=183112747)
            for i in range(len(photos['items'][0]['attachments'])):
                length = len(photos['items'][0]['attachments'][i]['photo']['sizes']) - 1
                print(photos['items'][0]['attachments'][i]['photo']['sizes'][length]['url'])
                urllib.request.urlretrieve(photos['items'][0]['attachments'][i]['photo']['sizes'][length]['url'],
                                           'C:/Users/user/Desktop/bot_silaedr/photos/' + str(i) + '.jpg')
            vko.messages.send(user_id=event.user_id,
                              random_id=random.randint(1, 10 ** 9),
                              message='Куда Вы хотите отправить новость?',
                              keyboard=create_keyb(['Группа ВК',  'Почта']))
            bred = False
            users[event.user_id] = 2
            continue
        if text == 'отправить':
            vko.messages.send(user_id=event.user_id,
                              random_id=random.randint(1, 10 ** 9),
                              message='Напишите мне, что Вы хотите разослать. При необходимости Вы можете прикрепить файлы к сообщению.',
                              keyboard=stop)
            flag = True
            users[event.user_id] = 1
            bred = False
        if 'привет' in text:
            if vko.users.get(user_ids=event.user_id, fields=['sex'])[0]['sex'] == 2:
                vko.messages.send(user_id=event.user_id,
                                  random_id=random.randint(1, 10 ** 9),
                                  message='Привет, ' + (inf['first_name']) + ' ' +
                                  inf['last_name'] + '!' + ' Я рад, что ты мне написал!',
                                  keyboard=base)
            else:
                vko.messages.send(user_id=event.user_id,
                                  random_id=random.randint(1, 10 ** 9),
                                  message='Привет, ' + (inf['first_name']) + ' ' +
                                          inf['last_name'] + '!' + ' Я рад, что ты мне написала!',
                                  keyboard=base)
            bred = False
        if users[event.user_id] == 10:
            if 'родителям' in text:
                google.send_to_class(grade)
                contacts += google.contacts
                google.clear()
            elif 'ученикам' in text:
                google.send_to_children(grade)
                contacts += google.contacts
                google.clear()
            elif 'всем' in text:
                google.send_to_class(grade)
                google.send_to_children(grade)
                contacts += google.contacts
                google.clear()
            users[event.user_id] = 3
            vko.messages.send(user_id=event.user_id,
                              random_id=random.randint(1, 10 ** 9),
                              message='Вы хотите отправить новость еще кому-нибудь? Если хотите, то напишите кому еще надо отправить новость, а если хотите отправить новость ранее выбранным контактам, то нажмите на кнопку "Отправить ранее выбранным контактам".' +
                                      '\n' + 'Для отмены отправки нажмите на кнопку "Отменить отправку"',
                              keyboard=create_keyb(
                                  ['5 С', '6 С', '7 С', 'new_line', '7 Т', '8 Л', '9 С', 'new_line', 'Учителям',
                                   'Отправить ранее выбранным контактам']))
            continue
        if users[event.user_id] == 3:
            cont = False
            to_all = False
            bred = False
            grade = '0'
            google.auth()
            for i in range(len(text)):
                try:
                    # print(text[i])
                    grade = str(int(text[i])) + ' '
                    grade += text[i+2].upper()
                    print(grade)
                    break
                except:
                    pass
            if grade != '0':
                vko.messages.send(user_id=event.user_id,
                                  random_id=random.randint(1, 10 ** 9),
                                  message='Кому Вы хотите отправить новость?', keyboard=create_keyb(['Родителям(' + grade + ')', 'Ученикам(' + grade + ')', 'Всем(' + grade + ')']))
                cont = True
                users[event.user_id] = 10
            elif 'абсолютно всем' in text:
                google.send_to_all()
                contacts += google.contacts
                google.clear()
                to_all = True
            elif 'учителям' in text:
                google.send_to_teachers()
                contacts += google.contacts
                google.clear()
            else:
                google.send_to_some(event.text)
                contacts += google.contacts
                google.clear()
            if to_all:
                vko.messages.send(user_id=event.user_id,
                                  random_id=random.randint(1, 10 ** 9),
                                  message='Подтвердите отправку', keyboard=create_keyb(['Отправить новость']))
            elif not cont:
                vko.messages.send(user_id=event.user_id,
                                  random_id=random.randint(1, 10 ** 9),
                                  message='Вы хотите отправить новость еще кому-нибудь? Если хотите, то напишите кому еще надо отправить новость, а если хотите отправить новость ранее выбранным контактам, то нажмите на кнопку "Отправить ранее выбранным контактам".' +
                                          '\n' + 'Для отмены отправки нажмите на кнопку "Отменить отправку"',
                                  keyboard=create_keyb(['5 С', '6 С', '7 С', 'new_line', '7 Т', '8 Л', '9 С', 'new_line', 'Учителям', 'Отправить ранее выбранным контактам']))
        if text == 'почта' and users[event.user_id] == 2:
            vko.messages.send(user_id=event.user_id,
                              random_id=random.randint(1, 10 ** 9),
                              message='Кому Вы хотите отправить новость? Вы можете отправить новость всем родителям определенного класса с помощью кнопок снизу.' + '\n' +
                                      ' Также Вы можете отправить новость конкретным родителям, написав сообщение типа "маме <Имя ребенка> <Фамилия ребенка>" или "отцу <Имя ребенка> <Фамилия ребенка>".',
                              keyboard=create_keyb(['5 С', '6 С', '7 С', 'new_line', '7 Т', '8 Л', '9 С', 'new_line', 'Учителям', 'Абсолютно всем']))
            users[event.user_id] = 3
            bred = False
        if text == 'опубликовать новость' and users[event.user_id] == 2:
            photos = glob.glob("C:/Users/user/Desktop/bot_silaedr/photos/*.jpg")
            if photos != []:
                photo_list = upload.photo_wall(photos)
                attachment = ','.join('photo{owner_id}_{id}'.format(**item) for item in photo_list)
                api.wall.post(owner_id=owner_id, message=news, attachments=attachment)
            else:
                api.wall.post(owner_id=owner_id, message=news)
            f_group = True
            if not f_mail:
                vko.messages.send(user_id=event.user_id,
                                  random_id=random.randint(1, 10 ** 9),
                                  message='Новость выложена в группе Силаэдра в ВК! Вы хотите отправить ее еще куда-нибудь?',
                                  keyboard=create_keyb1(['Почта', 'new_line', 'Нет, спасибо']))
            else:
                f_group = False
                f_mail = False
                vko.messages.send(user_id=event.user_id,
                                  random_id=random.randint(1, 10 ** 9),
                                  message='Новость выложена в группе Силаэдра в ВК! Обращайтесь, когда появятся еще новости!',
                                  keyboard=base)
                users[event.user_id] = 0
                if contacts != []:
                    print(contacts)
                    sendmail(news, glob.glob("C:/Users/user/Desktop/bot_silaedr/photos/*.jpg"))
                contacts = []
                news = ''
                bred = False
                folder = 'C:/Users/user/Desktop/bot_silaedr/photos'
                for the_file in os.listdir(folder):
                    file_path = os.path.join(folder, the_file)
                    try:
                        if os.path.isfile(file_path):
                            os.unlink(file_path)
                        # elif os.path.isdir(file_path): shutil.rmtree(file_path)
                    except Exception as e:
                        print(e)
            bred = False
        if text == 'группа вк' and users[event.user_id] == 2:
            vko.messages.send(user_id=event.user_id,
                              random_id=random.randint(1, 10 ** 9),
                              message='Подтвердите публикацию новости',
                              keyboard=create_keyb(['Опубликовать новость']))
            bred = False
        if text == 'сайт' and users[event.user_id] == 2:
            vko.messages.send(user_id=event.user_id,
                              random_id=random.randint(1, 10 ** 9),
                              message='К сожалению, сайт Силаэдра пока не работает! Вы хотите отправить новость еще куда-нибудь?',
                              keyboard=create_keyb1(['Группа ВК', 'Сайт', 'Почта', 'new_line', 'Нет, спасибо']))
            bred = False
        if text == 'help' or text == 'помощь' or text == '/start' or text == '/help' or text == 'начать':
            vko.messages.send(user_id=event.user_id,
                              random_id=random.randint(1, 10 ** 9),
                              message='Мои функции:' + '\n' +
                                      '- напишите мне "Отправить" для автоматической рассылки новостей, далее следуйте моим указаниям' + '\n' +
                                      '- напишите мне "Привет", и я поздороваюсь с Вами',
                              keyboard=base)
            bred = False
        if bred:
            vko.messages.send(user_id=event.user_id,
                              random_id=random.randint(1, 10 ** 9),
                              message='Извините, я Вас не понимаю. ' + '\n' +
                                      'Мои функции:' + '\n' +
                                      '- напишите мне "Отправить" для автоматической рассылки новостей, далее следуйте моим указаниям' + '\n' +
                                      '- напишите мне "Привет", и я поздороваюсь с Вами',
                              keyboard=base)
        print(users)
    # except Exception as er:
    #    print(er)
    #    pass
