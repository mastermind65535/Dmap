import os
import time
import threading
from queue import Queue
import io

class DiskImager:
    def __init__(self, DRIVE: str, OUTPUT: str, buffer=16 * 1024 * 1024):
        self.DRIVE = str(DRIVE)
        self.OUTPUT = str(OUTPUT)
        self.BUFFER = int(buffer)

        self.verify()

        # Buffered I/O
        self.driveInstance = io.BufferedReader(open(self.DRIVE, "rb"), buffer_size=self.BUFFER)
        self.outputInstance = io.BufferedWriter(open(self.OUTPUT, "wb"), buffer_size=self.BUFFER)

    def verify(self):
        if os.path.exists(self.OUTPUT):
            raise FileExistsError("Output file already exists.")

    def Convert(self):
        start_time = time.time()
        total_read = 0
        queue = Queue(maxsize=128)

        stop_event = threading.Event()

        def reader():
            try:
                while not stop_event.is_set():
                    buffer = self.driveInstance.read(self.BUFFER)
                    if not buffer:
                        queue.put(None)
                        break
                    queue.put(buffer)
            except Exception as e:
                stop_event.set()
                print(f"\n[Error] Reader encountered an error: {e}")

        def writer():
            nonlocal total_read
            try:
                while not stop_event.is_set():
                    buffer = queue.get()
                    if buffer is None:
                        break
                    self.outputInstance.write(buffer)
                    self.outputInstance.flush()
                    total_read += len(buffer)
                    print(f"[+] Total read: {total_read} bytes{' ' * 30}", end='\r')
            except Exception as e:
                stop_event.set()
                print(f"\n[Error] Writer encountered an error: {e}")

        reader_thread = threading.Thread(target=reader)
        writer_thread = threading.Thread(target=writer)

        reader_thread.start()
        writer_thread.start()

        reader_thread.join()
        writer_thread.join()

        if stop_event.is_set():
            print("\n[!] Operation terminated due to an error.")
        else:
            end_time = time.time()
            total_time = end_time - start_time
            print(f"\nTotal time taken: {total_time:.2f} seconds")

        self.driveInstance.close()
        self.outputInstance.close()
