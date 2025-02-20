from abc import ABC, abstractmethod
from jsonschema import validate, exceptions

class ExerciseSchema(ABC):
    @property
    @abstractmethod
    def schema(self):
        """Абстрактное свойство, которое должно быть реализовано в каждом наследнике."""
        pass

    def validate(self, data):
        """Метод для валидации данных по схеме."""
        validate(instance=data, schema=self.schema)

    def construct_data(self, command):
        """
        Метод для пошагового создания данных для упражнения.
        Если метод не переопределен в классе-потомке, выводим сообщение о недоступности конструктора.
        """
        print("Конструктор для этого типа упражнений пока недоступен.")
        
        return None
    