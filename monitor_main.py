import psutil
from time import sleep, time
from botsender import send_warning
#from socketsender import send_warning
sleep_time = 1 # секунды
traffic_monitor_period = 60  # одна минута
traffic_monitor_threshold = 10**9  # один гигабайт в байтах
temperature_threshold = 50 #градусов Цельсия

def do_main_program():
    """
    опрашивает сеносоры температуры и измеряет скачанный траффик
    в случае превышения температуры отправляет предупреждение (пороги отправки берутся из характеристик сенсоров)
    в случае превышения траффика загрузки отправляет сообщение о ддос атаке (порог - один гигабайт в минуту)
    """
    send_warning(type_of_message='starting', measure=-1) # сообщение о старте программы
    initial_bytes_recv = psutil.net_io_counters().bytes_recv # запоминаем изначальное количество скачаных байт
    initial_bytes_recv_time = time() # начальное время для измерения траффика
    
    while True: # основная петля программы
        temps = psutil.sensors_temperatures() # считываем показатели сенсоров, помещаем их в структуру temps
        for name, entries in temps.items(): #пробегаем кортеж по именам сенсоров и их показателям
            for entry in entries : # пробегаем по показателям сенсора
                if float(entry.current) >= float(temperature_threshold) and float(entry.current) < float(entry.critical): # проверяем , что температура высокая, но не критическая
                    device_name = entry.label or name # выбираем название устройства для отображения, если в показателях не указано имя, берём его из структуры
                    send_warning('temperature_high', entry.current, name = device_name) # посылаем сообщение 
                if float(entry.current) == float(entry.critical): # проверяем, критическая ли температура
                    send_warning(type_of_message='temperature_critical', measure=entry.current) # посылаем сообщение
                    
        if time()-initial_bytes_recv_time >= traffic_monitor_period: # проверяем, прошло ли достаточное количество времени с момента последнего замера траффика
            traffic_delta = psutil.net_io_counters().bytes_recv- initial_bytes_recv # вычисляем дельту траффика
            if traffic_delta >= traffic_monitor_threshold: # если дельта больше чем порог
                send_warning(type_of_message='traffic_overload', measure=traffic_delta) # отсылаем сообщение
                initial_bytes_recv = psutil.net_io_counters().bytes_recv #изменяем изначально количество скачанных байт
            initial_bytes_recv_time = time() #изменяем начальное время

        sleep(sleep_time) 
