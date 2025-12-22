from abc import ABC, abstractmethod

from jsonschema import exceptions, validate


class ExerciseSchema(ABC):
    @property
    @abstractmethod
    def schema(self):
        """Abstract property that must be implemented in each subclass."""
        pass

    @abstractmethod
    def fill_default(self):
        """
        Returns the default data for this exercise type.
        Must be implemented in each subclass.
        """
        pass

    def validate(self, data):
        """Method to validate data against the schema."""
        validate(instance=data, schema=self.schema)
