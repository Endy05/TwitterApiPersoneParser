from queue import Queue
from typing import Dict, Any, Callable
from datetime import datetime
import threading
import time

class ThreadManager:
    def __init__(self):
        self.threads: Dict[str, threading.Thread] = {}
        self.queues: Dict[str, Queue] = {}
        self.running = False
        self.last_run: Dict[str, float] = {}

    def add_worker(self, name: str, worker_func: Callable, interval: float = 5):
        """Add a new worker thread"""
        queue = Queue()
        self.queues[name] = queue
        self.last_run[name] = 0

        def worker_wrapper():
            while self.running:
                current_time = time.time()
                time_since_last_run = current_time - self.last_run[name]
                
                # Wait for the exact interval
                if time_since_last_run < interval:
                    time.sleep(interval - time_since_last_run)
                
                try:
                    result = worker_func()
                    if result:
                        self.queues[name].put(result)
                except Exception as e:
                    print(f"Error in worker {name}: {e}")
                
                self.last_run[name] = time.time()

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
