#from pyspectator.processor import Cpu
import psutil
import sys
from time import sleep, time
from botsender import send_warning
#from socketsender import send_warning
sleep_time = 1 # секунды
traffic_monitor_period = 60  # одна минута
traffic_monitor_threshold = 10**9  # один гигабайт в байтах
temperature_threshold = 50

def do_main_program():
    """
    опрашивает сеносоры температуры и измеряет скачанный траффик
    в случае превышения температуры отправляет предупреждение (пороги отправки берутся из характеристик сенсоров)
    в случае превышения траффика загрузки отправляет сообщение о ддос атаке (порог - один гигабайт в минуту)
    TODO: 'передавать id девайса который перегрелся'

    """
    send_warning(type_of_message='starting', measure=-1)
    initial_bytes_recv = psutil.net_io_counters().bytes_recv
    initial_bytes_recv_time = time()
    #
    # if not hasattr(psutil, "sensors_temperatures"):
    #     sys.exit("platform not supported")
    # if not hasattr(psutil, "net_io_counters"):
    #     sys.exit("platform not supported")
    while True:
        temps = psutil.sensors_temperatures()
        # if not temps:
        #     sys.exit("can't rea   d any temperature")
        for name, entries in temps.items():
            for entry in entries :
                # if entry.label.startswith('Package'):
                # print("    %-20s %s °C (high = %s °C, critical = %s °C)" % (
                #     entry.label or name, entry.current, entry.high,
                #     entry.critical))
                if float(entry.current) >= float(temperature_threshold) and float(entry.current) < float(entry.critical):
                    device_name = entry.label or name
                    # overheated_name = {name: device_name}
                    send_warning('temperature_high', entry.current, name = device_name)
                if float(entry.current) == float(entry.critical):
                    send_warning(type_of_message='temperature_critical', measure=entry.current)
        if time()-initial_bytes_recv_time >= traffic_monitor_period:
            traffic_delta = psutil.net_io_counters().bytes_recv- initial_bytes_recv
            if traffic_delta >= traffic_monitor_threshold:
                send_warning(type_of_message='traffic_overload', measure=traffic_delta)
                initial_bytes_recv = psutil.net_io_counters().bytes_recv
            initial_bytes_recv_time = time()

        sleep(sleep_time)


if __name__ == '__main__':
    do_main_program()