from CryptoData import BigIntData, CryptoData, CryptoDataArray
from ZKProtocol import ZKProtocol
from PedersenCommitment import PedersenCommitment

class SchnorrProtocolProveSecretKey(ZKProtocol):
    def __init__(self, config):
        self.p = config.p
        self.q = config.q
        self.g = config.g
        self.h = config.h
        self.y = config.y
        self.p1 = None
        self.a = None
        self.x = None
        self.simz1 = None
        self.pedersen_commitment = PedersenCommitment(self.p, self.g, self.h)

    def commitment(self, secrets: CryptoData) -> CryptoData:
        if secrets:
            self.x = secrets.get_big_int()

        self.p1 = self.pedersen_commitment.generate_commitment(self.p, 0)
        self.a = pow(self.g, self.p1, self.p)
        return CryptoDataArray([
            BigIntData(self.a),
            BigIntData(self.pedersen_commitment.generate_commitment(self.x, 0))
        ])

    def simcommitment(self, secrets: CryptoData, c2: int, z2: CryptoData) -> CryptoData:
        if secrets:
            self.x = secrets.get_big_int()

        commit = self.pedersen_commitment.generate_commitment(self.x, 0)
        z_array = z2.get_crypto_data_array()
        self.simz1 = z_array[0].get_big_int()
        self.a = self.pedersen_commitment.generate_simcommitment(self.simz1, 0, commit, c2)
        return CryptoDataArray([
            BigIntData(self.a),
            BigIntData(commit)
        ])

    def determine_proof(self, challenge: int) -> CryptoData:
        z = (self.p1 + challenge * self.x) % (self.p - 1)
        return CryptoDataArray([
            BigIntData(z),
            BigIntData(challenge)
        ])

    def simdetermine_proof(self, challenge: int) -> CryptoData:
        return CryptoDataArray([
            BigIntData(self.simz1),
            BigIntData(challenge)
        ])

    def verify(self, proofs: CryptoData, other_variables: CryptoData) -> bool:
        a = other_variables.get_crypto_data_array()[0].get_big_int()
        y = other_variables.get_crypto_data_array()[1].get_big_int()
        z = proofs.get_crypto_data_array()[0].get_big_int()
        challenge = proofs.get_crypto_data_array()[1].get_big_int()

        lhs = self.pedersen_commitment.generate_commitment(z, 0)
        rhs = (a * pow(y, challenge, self.p)) % self.p

        return lhs == rhs

    def simverify(self, proofs: CryptoData, other_variables: CryptoData) -> bool:
        pass

    def simallcommitment(self, protocol: 'ZKProtocol', secrets: CryptoData, c2: int, z2: CryptoData) -> CryptoData:
        raise NotImplementedError("Unimplemented method 'simallcommitment'")
