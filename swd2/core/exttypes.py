import enum
import json


class Objects:
    @staticmethod
    def toJson(value) -> str:
        if isinstance(value, set):
            return Objects.toJson(list(value))
        if isinstance(value, enum.Enum):
            return value.name
        return json.dumps(value, default=lambda o: o.__dict__ if hasattr(o, '__dict__') else {}, sort_keys=True, indent=1, check_circular=True)


class ExtObject:
    # def __eq__(self, other) -> bool:
    #     return Objects.equals(self, other)
    #
    # def __hash__(self) -> int:
    #     return Objects.hash(self)

    def __str__(self) -> str:
        return Objects.toJson(self)


class ExtEnum(ExtObject, enum.Enum):
    @classmethod
    def elements(cls) -> dict:
        return cls.__members__

    @classmethod
    def values(cls):
        return cls.elements().items()

    @classmethod
    def of(cls, predicate: callable):
        for el in cls.elements().values():
            if predicate(el):
                return el
        raise NoSuchElementException(f'There is not element that match the predicate.')

    @classmethod
    def ofName(cls, name):
        try:
            return cls.of(lambda element: element.name == name)
        except NoSuchElementException as e:
            raise NoSuchElementException(
                f'Element [{name}] not exists for [{cls}]. Possible values are [{", ".join(cls.elements().keys())}]')

    @classmethod
    def ofValue(cls, value):
        try:
            return cls.of(lambda element: element.value == value)
        except NoSuchElementException as e:
            raise NoSuchElementException(
                f'Element [{value}] not exists for [{cls}]. Possible values are [{str(cls.elements().values())}]')

    def __str__(self) -> str:
        return str(self.name)


class NoSuchElementException(Exception):
    def __init__(self, message):
        self.message = message
