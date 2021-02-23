"""Кастомные исключения для mixins"""


class WrongModelSubClassException(Exception):
    pass


class NoModuleAttributeException(Exception):
    pass
