import daemon
from monitor_main import do_main_program
# from botsender import send_warning

with daemon.DaemonContext():
    do_main_program()
