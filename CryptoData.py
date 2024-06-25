from abc import ABC, abstractmethod
from typing import List, Optional

class CryptoData(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def get_big_int(self) -> Optional[int]:
        pass

    @abstractmethod
    def get_crypto_data_array(self) -> Optional[List['CryptoData']]:
        pass

    @abstractmethod
    def has_null(self) -> bool:
        pass

    def print_values(self, level: int = 0) -> None:
        indent = "  " * level
        if isinstance(self, BigIntData):
            value = self.get_big_int()
            print(indent + f"BigIntData: {value if value is not None else 'null'}")
        elif isinstance(self, CryptoDataArray):
            array = self.get_crypto_data_array()
            if array is not None:
                print(indent + "CryptoDataArray: [")
                for data in array:
                    if data is not None:
                        data.print_values(level + 1)
                    else:
                        print(indent + "  null")
                print(indent + "]")
            else:
                print(indent + "CryptoDataArray: null")

class BigIntData(CryptoData):
    def __init__(self, value: Optional[int]):
        super().__init__()
        self.value = value

    def get_big_int(self) -> Optional[int]:
        return self.value

    def get_crypto_data_array(self) -> Optional[List[CryptoData]]:
        return None

    def has_null(self) -> bool:
        return self.value is None

class CryptoDataArray(CryptoData):
    def __init__(self, array: Optional[List[CryptoData]]):
        super().__init__()
        self.array = array

    def get_big_int(self) -> Optional[int]:
        return None

    def get_crypto_data_array(self) -> Optional[List[CryptoData]]:
        return self.array

    def has_null(self) -> bool:
        if self.array:
            return any(data is None or data.has_null() for data in self.array)
        return True
