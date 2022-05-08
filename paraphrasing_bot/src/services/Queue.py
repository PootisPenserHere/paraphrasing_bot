import queue


def queue_to_list(items_queue: queue) -> list:
    items = []
    while items_queue.qsize():
        current = items_queue.get()
        items.append(current)

    return items
