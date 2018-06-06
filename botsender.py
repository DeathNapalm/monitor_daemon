import telegram
from credentials import tokens


def send_warning(type_of_message, measure,*args, **kvargs):
    """
    отправляет сообщение пользователю от лица телеграм бота
    тип сообщения может быть предупреждением о превышении температуры цп или о превышении траффика загрузки
    дополнительно сообщает о размере превышения
    """
    message_decoder = {'temperature_high': 'температура устройства {name_dev} высокая и составляет {measure_dev}',
                       'temperature_critical': 'температура устройства {name_dev} критическая и составляет {measure_dev}',
                       'traffic_overload': 'устройство превысило порог загрузки и загрузило {measure_dev} байт за минуту',
                       'starting': 'демон запущен'}
    chat_id_token = tokens['chat_id']
    proxy_server = telegram.utils.request.Request(proxy_url=tokens['proxy_url'])
    bot = telegram.Bot(token=tokens['token'], request=proxy_server)
    bot.send_message(chat_id=chat_id_token, text=message_decoder[type_of_message].format(name_dev=kvargs.pop('name',''), measure_dev=str(measure)))

