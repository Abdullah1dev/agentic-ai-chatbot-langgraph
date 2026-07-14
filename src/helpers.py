import uuid


def generate_threadid():
    thread_id = uuid.uuid4()
    return str(thread_id)