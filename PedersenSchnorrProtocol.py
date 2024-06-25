from CryptoData import BigIntData, CryptoData, CryptoDataArray
from ZKProtocol import ZKProtocol # type: ignore
from Utils import generate_random
from PedersenCommitment import PedersenCommitment # type: ignore

class PedersenSchnorrProtocol(ZKProtocol):
    def __init__(self, config):
        self.p = config.p
        self.q = config.q
        self.g = config.g
        self.h = config.h
        self.y = config.y
        self.p1 = None
        self.p2 = None
        self.a = None
        self.m = None
        self.r1 = None
        self.simz1 = None
        self.simz2 = None
        self.pedersen_commitment = PedersenCommitment(self.p, self.g, self.h)


    def commitment(self, secrets: CryptoData) -> CryptoData:
        if secrets and secrets.get_crypto_data_array():
            self.m = secrets.get_crypto_data_array()[0].get_big_int()
            self.r1 = secrets.get_crypto_data_array()[1].get_big_int()
        else:
            self.m = 0
            self.r1 = 0
            
        self.p1 = generate_random(self.p)
        self.p2 = generate_random(self.p)
        self.a = self.pedersen_commitment.generate_commitment(self.p1, self.p2)
        return CryptoDataArray([
            BigIntData(self.a),
            BigIntData(self.pedersen_commitment.generate_commitment(self.m, self.r1))
        ])

    def simcommitment(self, secrets: CryptoData, c2: int, z2: CryptoData) -> CryptoData:
        if secrets and secrets.get_crypto_data_array():
            self.m = secrets.get_crypto_data_array()[0].get_big_int()
            self.r1 = secrets.get_crypto_data_array()[1].get_big_int()
        else:
            self.m = 0
            self.r1 = 0

        commit = self.pedersen_commitment.generate_commitment(self.m, self.r1)
        z_array = z2.get_crypto_data_array()
        self.simz1 = z_array[0].get_big_int()
        self.simz2 = z_array[1].get_big_int()
        self.a = self.pedersen_commitment.generate_simcommitment(self.simz1, self.simz2, commit, c2)

        return CryptoDataArray([
            BigIntData(self.a),
            BigIntData(commit)
        ])

    def determine_proof(self, challenge: int) -> CryptoData:
        z1 = (self.p1 + challenge * self.m) % (self.p - 1)
        z2 = (self.p2 + challenge * self.r1) % (self.p - 1)
        return CryptoDataArray([
            CryptoDataArray([
                BigIntData(z1),
                BigIntData(z2)
            ]),
            BigIntData(challenge)
        ])

    def simdetermine_proof(self, challenge: int) -> CryptoData:
        return CryptoDataArray([
            CryptoDataArray([
                BigIntData(self.simz1),
                BigIntData(self.simz2),
            ]),
            BigIntData(challenge)
        ])

    def verify(self, proofs: CryptoData, other_variables: CryptoData) -> bool:
        a = other_variables.get_crypto_data_array()[0].get_big_int()
        c = other_variables.get_crypto_data_array()[1].get_big_int()
        z1 = proofs.get_crypto_data_array()[0].get_crypto_data_array()[0].get_big_int()
        z2 = proofs.get_crypto_data_array()[0].get_crypto_data_array()[1].get_big_int()
        challenge = proofs.get_crypto_data_array()[1].get_big_int()

        lhs = self.pedersen_commitment.generate_commitment(z1, z2)
        rhs = (a * pow(c, challenge, self.p)) % self.p

        return lhs == rhs

    def simverify(self, proofs: CryptoData, other_variables: CryptoData) -> bool:
        pass

    def simallcommitment(self, protocol: 'ZKProtocol', secrets: CryptoData, c2: int, z2: CryptoData) -> CryptoData:
        raise NotImplementedError("Unimplemented method 'simallcommitment'")
