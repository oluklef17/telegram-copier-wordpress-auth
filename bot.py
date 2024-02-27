from gui import queue_in, queue_out, ui
from threading import Thread


def run_bot():
    while True:
        try:
            if not queue_in.empty():
                cmd = queue_in.get()
                if cmd == 'ui launched':
                    ui.stackedWidget.setCurrentIndex(1)
                    break
        except KeyboardInterrupt:
            print('Done')
            break


bot_thread = Thread(target=run_bot)
bot_thread.start()

