import os
from functools import wraps
from datetime import datetime


# Параметризованный декоратор
def logger(path):
    def __logger(old_function):
        @wraps(old_function)
        def new_function(*args, **kwargs):
            result = old_function(*args, **kwargs)
            with open(path, 'a', encoding='utf-8') as f:
                f.write(
                    f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | "
                    f"{old_function.__name__} | "
                    f"args: {args}, kwargs: {kwargs} | "
                    f"return: {result}\n"
                )
            return result
        return new_function
    return __logger


class FlatIterator:

    def __init__(self, list_of_list):
        self.list_of_list = list_of_list
        self.flat_list = []
        self._flatten(self.list_of_list)
        self.index = 0

    @logger('flat_iterator.log')   # Логируем процесс рекурсивного разворачивания
    def _flatten(self, items):
        for item in items:
            if isinstance(item, list):
                self._flatten(item)
            else:
                self.flat_list.append(item)

    def __iter__(self):
        self.index = 0
        return self

    @logger('flat_iterator.log')   # Логируем выдачу элементов через __next__
    def __next__(self):
        if self.index >= len(self.flat_list):
            raise StopIteration
        item = self.flat_list[self.index]
        self.index += 1
        return item


def test_3():

    list_of_lists_2 = [
        [['a'], ['b', 'c']],
        ['d', 'e', [['f'], 'h'], False],
        [1, 2, None, [[[[['!']]]]], []]
    ]

    for flat_iterator_item, check_item in zip(
            FlatIterator(list_of_lists_2),
            ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None, '!']
    ):
        assert flat_iterator_item == check_item

    assert list(FlatIterator(list_of_lists_2)) == [
        'a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None, '!'
    ]


if __name__ == '__main__':
    test_3()