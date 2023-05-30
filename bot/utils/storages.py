from collections import deque
from datetime import datetime, timedelta
from typing import TypeVar

_KT = TypeVar("_KT")
_VT = TypeVar("_VT")


class TmpStorage(dict):
    """
    Створює репозиторій для тимчасового сховища будь-яких об'єктів (наприклад, клавіатура, що має зберегти свій
    стан між викликами хендлерів).

    Сховище поводиться як звичайний словник.
    При створенні сховища можуть бути задані три базових параметри сховища:
    - max_number_of_elements: int - максимальна місткість сховища
    - min_lifetime_sec: int - мінімальний час зберігання елемента (сигнальний параметр)
    - max_lifetime_sec: int - максимальний час зберігання елемента
    """

    def __init__(
        self,
        max_number_of_elements: int = 32,
        min_lifetime_sec: int = 900,
        max_lifetime_sec: int = 84600,
    ) -> None:
        self.max_number_of_elements = max_number_of_elements
        self.min_lifetime = timedelta(seconds=min_lifetime_sec)
        self.max_lifetime = timedelta(seconds=max_lifetime_sec)
        self._deque = deque("")
        self._creation_time: dict = {}

    def __setitem__(self, __key: _KT, __value: _VT) -> None:
        """Перевіряє наявність елемента з заданим ключем,
        якщо є:
            - перезаписує час внесення в сховище елемента з заданим ключем (self._creation_time)
            - видаляє наявний ключ з черги (self._deque)
            - записує ключ в початок черги (self._deque)
            - перезаписує значення в словнику для цього ключа з новим значенням
        якщо немає:
            - записує час внесення в сховище елемента з заданим ключем (self._creation_time)
            - записує ключ в початок черги (self._deque)
            - записує значення для заданого ключа в словник
            - якщо загальна довжина черги більше ніж self.max_number_of_element, то:
                - 'забирає' (отримує та видаляє) з кінця черги ключ
                - видаляє елемент з 'отриманим' ключем зі словника
                - читає для отриманого ключа час створення. Якщо час його життя менший ніж self.min_lifetime, формує
                  в лог попередження
                - видаляє елемент для цього ключа в self._creation_time
        """
        if __key in self._deque:
            self._deque.remove(__key)
        self._creation_time[__key] = datetime.now()
        self._deque.append(__key)
        if len(self._deque) > self.max_number_of_elements:
            key_for_del = self._deque.popleft()
            if datetime.now() - self._creation_time[key_for_del] < self.min_lifetime:
                print(
                    f"WARNING: in object {self} deleted element with key = {key_for_del}. \
    The lifetime of this element is less than {self.min_lifetime}. You may need to increase the storage size."
                )
                self.__delitem__(__key)
        return super().__setitem__(__key, __value)

    def __getitem__(self, __key: _KT) -> _VT:
        """Повертає елемент зі сховища за його ключем, якщо час існування цього існування менший ніж self.max_lifetime.

        - перевіряє наявність ключа та в разі відсутності створює виняток KeyError
        - за ключем зчитує з self._creation_time час внесення елемента в сховище
        - якщо час існування елемента на поточний момент перевищує self.max_lifetime, то:
            - за ключем видаляє:
                - елемент зі словника
                - час внесення елементу в сховище self._creation_time
                - ключ із черги
                - створює виняток KeyError з відповідним повідомленням
        """
        try:
            result = super().__getitem__(__key)
            if datetime.now() - self._creation_time[__key] > self.max_lifetime:
                self.__delitem__(__key)
                raise KeyError(
                    f"The {result} object (key={__key}) has been removed from the storage \
                because the storage interval for the object has been exceeded."
                )
            return result
        except KeyError:
            print(f"The key {__key} is missing in the object {self}.")

    def __delitem__(self, __key: _KT) -> None:
        """Видаляє елемент зі словника і всі супутні елементи:
        - перевіряє наявність ключа і в разі відсутності створює виняток KeyError
        - час внесення елемента в сховище
        - ключ із черги
        """
        try:
            super().__delitem__(__key)
            del self._creation_time[__key]
            self._deque.remove(__key)
        except KeyError:
            print(f"The key {__key} is missing in the object {self}.")
            raise
        except ValueError:
            pass
