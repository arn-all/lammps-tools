import threading
import time

class AnimationHandler:
    def __init__(self):
        self.animation_chars = ["⢿", "⣻", "⣽", "⣾", "⣷", "⣯", "⣟", "⡿"]
        self.done_flag = threading.Event()

    def animate_progress(self, func):
        def wrapper(*args, **kwargs):
            animation_thread = threading.Thread(target=self._animate)
            animation_thread.start()

            try:
                func(*args, **kwargs)
            finally:
                self.done_flag.set()
                animation_thread.join()

        return wrapper

    def _animate(self):
        i = 0
        while not self.done_flag.is_set():
            print(f'\rConverting... {self.animation_chars[i]}', end='', flush=True)
            i = (i + 1) % len(self.animation_chars)
            time.sleep(0.1)

animation_handler = AnimationHandler()
animate_progress = animation_handler.animate_progress
