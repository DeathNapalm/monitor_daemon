import daemon
from monitor_main import do_main_program

with daemon.DaemonContext():
    do_main_program()
