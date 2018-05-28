import socket
from time import sleep
serversocket = socket.socket()

host = ''
port = 50007

serversocket.bind(('', port))
serversocket.listen(1)


def send_warning(type_of_message, measure,*args, **kvargs):
    if type_of_message == 'temperature_high':
        text_of_message = 'температура устройства {} высокая и составляет {}'.format(kvargs['name'], str(measure))
        clientsocket, addr = serversocket.accept()
        clientsocket.send(text_of_message.encode('UTF-8'))
        clientsocket.close()
    if type_of_message == 'temperature_critical':
        text_of_message = 'температура устройства {} критическая и составляет {}'.format(kvargs['name'], str(measure))
        clientsocket, addr = serversocket.accept()
        clientsocket.send(text_of_message.encode('UTF-8'))
        clientsocket.close()
    if type_of_message == 'traffic_overload':
        text_of_message = 'устройство превысило порог загрузки и загрузило {} байт за минуту'.format(str(measure))
        clientsocket, addr = serversocket.accept()
        clientsocket.send(text_of_message.encode('UTF-8'))
        clientsocket.close()
    if type_of_message == 'starting': # системное сообщение. measure можно использовать для кодов
        text_of_message = 'демон запущен'
        clientsocket, addr = serversocket.accept()
        clientsocket.send(text_of_message.encode('UTF-8'))
        clientsocket.close()
# while True:
#     clientsocket,addr = serversocket.accept()
#     print("got a connection from %s" % str(addr))
#
#     msg = 'Thank you for connecting' + "\r\n"
#     clientsocket.send(msg.encode('ascii'))
#     clientsocket.close()