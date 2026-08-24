from abc import ABC, abstractmethod
from typing import Generic, TypeVar


class ConfigValueConstraintResult:
    def __init__(self, error_message: str | None = None, translation_key: str | None = None, translation_params: dict[str, str | int] | None = None) -> None:
        self.__error_message: str | None = error_message
        self.__translation_key = translation_key
        self.__translation_params = translation_params or {}

    @property
    def is_success(self) -> bool:
        return self.__error_message == None
    
    @property
    def error_message(self) -> str:
        if self.__error_message:
            return self.__error_message
        else:
            return ""

    @property
    def translation_key(self) -> str | None:
        return self.__translation_key

    @property
    def translation_params(self) -> dict[str, str | int]:
        return self.__translation_params

T = TypeVar('T')
class ConfigValueConstraint(Generic[T], ABC):
    def __init__(self, description: str | None = None) -> None:
        super().__init__()
        self.__description: str = description
    
    @property
    def description(self) -> str:
        return self.__description
    
    @abstractmethod
    def apply_constraint(self, value_to_apply_to: T) -> ConfigValueConstraintResult:
        pass