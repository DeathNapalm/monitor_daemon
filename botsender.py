import telegram


def send_warning(type_of_message, measure,*args, **kvargs):
    """
    отправляет сообщение пользователю от лица телеграм бота
    тип сообщения может быть предупреждением о превышении температуры цп или о превышении траффика загрузки
    дополнительно сообщает о размере превышения
    """
    proxy_server = telegram.utils.request.Request(proxy_url='')
    bot = telegram.Bot(token=, request=proxy_server)
    if type_of_message == 'temperature_high':
        text_of_message = 'температура устройства {} высокая и составляет {}'.format(kvargs['name'], str(measure))
        bot.send_message(chat_id=, text=text_of_message)
    if type_of_message == 'temperature_critical':
        text_of_message = 'температура устройства {} критическая и составляет {}'.format(kvargs['name'], str(measure))
        bot.send_message(chat_id=, text=text_of_message)
    if type_of_message == 'traffic_overload':
        text_of_message = 'устройство превысило порог загрузки и загрузило {} байт за минуту'.format(str(measure))
        bot.send_message(chat_id=, text=text_of_message)
    if type_of_message == 'starting': # системное сообщение. measure можно использовать для кодов
        text_of_message = 'демон запущен'
        bot.send_message(chat_id=, text=text_of_message)
