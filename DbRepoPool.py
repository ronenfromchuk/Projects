from DbRepo import DbRepo
from db_config import local_session
import threading
import time


class DbRepoPool:
    _instance = None
    _lock = threading.Lock()
    _lock_pool = threading.Lock()
    _max_connections = 20

    def __init__(self):
        raise RuntimeError('call instance() instead')

    @classmethod
    def get_instance(cls):
        if cls._instance:
            return cls._instance
        with cls._lock:
            if cls._instance is None:
                cls._instance = cls.__new__(cls)
                cls._instance.connections = [DbRepo(local_session)
                                             for i in range(cls._max_connections)]
            return cls._instance

    def get_available_count(self):
        return len(self.connections)

    @staticmethod
    def get_max_possible_connections():
        return DbRepoPool._max_connections

    def get_connection(self):
        while True:
            if len(self.connections) == 0:
                time.sleep(0.2)
                continue
            with self._lock_pool:
                if len(self.connections) > 0:
                    return self.connections.pop(0)

    def return_connection(self, conn):

        with self._lock_pool:
            self.connections.append(conn)