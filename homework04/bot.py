import requests
import config
import telebot
from bs4 import BeautifulSoup
from datetime import datetime

weekdays = {'/monday': '1', '/tuesday': '2', '/wednesday': '3', '/thursday': '4', '/friday': '5', '/saturday': '6',
            '/sunday': '1'}
weekdays_rus = {1: 'Понедельник', 2: 'Вторник', 3: 'Среда', 4: 'Четверг', 5: 'Пятница', 6: 'Суббота'}

telebot.apihelper.proxy = {'https': 'https://209.90.63.108:80'}
bot = telebot.TeleBot(config.access_token)


def get_page(group, week=''):
    if week:
        week = str(week) + '/'
    url = '{domain}/{group}/{week}raspisanie_zanyatiy_{group}.htm'.format(
        domain=config.domain,
        week=week,
        group=group)
    response = requests.get(url)
    web_page = response.text
    return web_page


def parse_schedule(web_page, day):
    soup = BeautifulSoup(web_page, "html5lib")

    # Получаем таблицу с расписанием на день
    schedule_table = soup.find("table", attrs={"id": day + "day"})

    if schedule_table is None:
        return False
    else:
        # Время проведения занятий
        times_list = schedule_table.find_all("td", attrs={"class": "time"})
        times_list = [time.span.text for time in times_list]

        # Место проведения занятий
        locations_list = schedule_table.find_all("td", attrs={"class": "room"})
        locations_list = [room.span.text for room in locations_list]

        # Аудитория
        classrooms_list = schedule_table.find_all("td", attrs={"class": "room"})
        classrooms_list = [classroom.dd.text for classroom in classrooms_list]

        # Название дисциплин и имена преподавателей
        lessons_list = schedule_table.find_all("td", attrs={"class": "lesson"})
        lessons_list = [lesson.text.split() for lesson in lessons_list]
        lessons_list = [' '.join([info for info in lesson_info if info]) for lesson_info in lessons_list]

        return times_list, locations_list, classrooms_list, lessons_list


@bot.message_handler(commands=['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'])
def get_schedule(message):
    """ Получить расписание на указанный день """
    day, group, week = message.text.split()
    day = weekdays[day]

    web_page = get_page(group, week)
    if not check_web_page(week, web_page):
        resp = 'Расписание не найдено'
        bot.send_message(message.chat.id, resp, parse_mode='HTML')
        return

    test = parse_schedule(web_page, day)
    if not test:
        resp = 'Занятий нет'
    else:
        times_list, locations_list, classrooms_list, lessons_list = test
        resp = ''
        for time, location, classroom, lesson in zip(times_list, locations_list, classrooms_list, lessons_list):
            resp += '<b>{}</b>, {}, {}, {}\n'.format(time, location, classroom, lesson)
    bot.send_message(message.chat.id, resp, parse_mode='HTML')


@bot.message_handler(commands=['near'])
def get_near_lesson(message):
    """ Получить ближайшее занятие """
    _, group, week = message.text.split()
    web_page = get_page(group, week)

    if not check_web_page(week, web_page):
        resp = 'Расписание не найдено'
        bot.send_message(message.chat.id, resp, parse_mode='HTML')
        return

    day = list(weekdays.values())[datetime.weekday(datetime.now())]
    test = parse_schedule(web_page, day)

    if not test:
        resp = 'Сегодня занятий нет вообще'
    else:
        times_list, locations_list, classrooms_list, lessons_list = test
        curr_hour = datetime.time(datetime.now()).hour
        curr_min = datetime.time(datetime.now()).minute
        resp = ''

        for time in times_list:
            start_hour, start_min = int(time[:2]), int(time[3:5])
            fin_hour, fin_min = int(time[6:8]), int(time[9:])
            if start_hour < curr_hour < fin_hour or curr_hour == start_hour and start_min < curr_min \
                    or curr_hour == fin_hour and fin_min > curr_min:
                ind = times_list.index(time)
                resp = 'Сейчас идет пара\n\n<b>{}</b>, {}, {}\n'.format(time, locations_list[ind], classrooms_list[ind],
                                                                        lessons_list[ind])
                break
            if start_hour > curr_hour or start_hour == curr_hour and start_min > curr_min:
                ind = times_list.index(time)
                resp = 'Следующая пара\n\n<b>{}</b>, {}, {}\n'.format(time, locations_list[ind], classrooms_list[ind],
                                                                      lessons_list[ind])
                break

        if resp == '':
            resp = 'Сегодня больше занятий нет'
    bot.send_message(message.chat.id, resp, parse_mode='HTML')


@bot.message_handler(commands=['tomorrow'])
def get_tomorrow(message):
    """ Получить расписание на следующий день """
    message.text = list(weekdays.keys())[datetime.weekday(datetime.now()) + 1] + message.text[9:]
    get_schedule(message)


@bot.message_handler(commands=['all'])
def get_all_schedule(message):
    """ Получить расписание на всю неделю для указанной группы """
    temp = message.text[4:]
    for day in list(weekdays.keys())[:len(weekdays) - 1]:
        message.text = day + temp
        bot.send_message(message.chat.id, weekdays_rus[int(weekdays[day])], parse_mode='HTML')
        get_schedule(message)


def check_web_page(week, web_page):
    if week not in ('0', '1', '2'):
        return False
    soup = BeautifulSoup(web_page, "html5lib")
    check_items = soup.find_all("article", attrs={"class": "content_block", "style": "position:relative;"})
    for item in check_items:
        if 'Расписание не найдено' in item.text:
            return False
    return True


if __name__ == '__main__':
    bot.polling(none_stop=True)
