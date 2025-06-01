import threading
from queue import Queue
from typing import Dict, Any, Callable
import time
from datetime import datetime

class ThreadManager:
    def __init__(self):
        self.threads: Dict[str, threading.Thread] = {}
        self.queues: Dict[str, Queue] = {}
        self.running = False
        self.loop = None

    def add_worker(self, name: str, worker_func: Callable, interval: int = 5):
        """Add a new worker thread"""
        queue = Queue()
        self.queues[name] = queue

        def worker_wrapper():
            while self.running:
                try:
                    result = worker_func()
                    if result:  # Only log if we got actual results
                        current_time = datetime.now().strftime("%H:%M:%S")
                        print(f"[{current_time}] {name.capitalize()} received")
                    queue.put(result)
                except Exception as e:
                    print(f"Error in {name} thread: {e}")
                time.sleep(interval)

        thread = threading.Thread(target=worker_wrapper, name=name, daemon=True)
        self.threads[name] = thread

    def start(self):
        """Start all worker threads"""
        self.running = True
        for thread in self.threads.values():
            thread.start()

    def stop(self):
        """Stop all worker threads"""
        self.running = False
        for thread in self.threads.values():
            thread.join()

    def get_result(self, name: str) -> Any:
        """Get result from worker queue"""
        try:
            return self.queues[name].get_nowait()
        except:
            return None
