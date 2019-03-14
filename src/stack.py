from src.models import Queue

def run():
    while True:
        task = Queue.pop()

        if not task:
            continue

        print(task)

if __name__ == "__main__":
    run()