from abc import ABC, abstractmethod
from CryptoData import CryptoData

class ZKProtocol(ABC):
    @abstractmethod
    def commitment(self, secrets: CryptoData) -> CryptoData:
        pass

    @abstractmethod
    def simcommitment(self, secrets: CryptoData, c2: int, z2: CryptoData) -> CryptoData:
        pass

    @abstractmethod
    def simallcommitment(self, protocol: 'ZKProtocol', secrets: CryptoData, c2: int, z2: CryptoData) -> CryptoData:
        pass

    @abstractmethod
    def determine_proof(self, challenge: int) -> CryptoData:
        pass

    @abstractmethod
    def simdetermine_proof(self, challenge: int) -> CryptoData:
        pass

    @abstractmethod
    def verify(self, proofs: CryptoData, other_variables: CryptoData) -> bool:
        pass

    @abstractmethod
    def simverify(self, proofs: CryptoData, other_variables: CryptoData) -> bool:
        pass
