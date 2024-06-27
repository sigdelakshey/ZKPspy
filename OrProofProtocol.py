from CryptoData import BigIntData, CryptoData, CryptoDataArray
from ZKProtocol import ZKProtocol
from Utils import generate_random 

class OrProofProtocol(ZKProtocol):
    def __init__(self, config, protocols):
        self.protocols = protocols
        self.p = config.p
        self.q = config.q
        self.g = config.g
        self.h = config.h
        self.y = config.y
        self.c1 = None
        self.c2 = None
        self.z2 = None

    def commitment(self, secrets: CryptoData) -> CryptoData:
        self.c2 = generate_random(self.p)            
        z2_1 = generate_random(self.p)
        z2_2 = generate_random(self.p)
        z2 = CryptoDataArray([BigIntData(z2_1), BigIntData(z2_2)])

        commitments = []
        for i, protocol_set in enumerate(self.protocols):
            protocol_commitments = []
            for j, protocol in enumerate(protocol_set):
                if i == 1:
                    # Simulate commitment for the second set
                    secret = secrets.get_crypto_data_array()[i].get_crypto_data_array()[j]
                    protocol_commitments.append(protocol.simcommitment(secret,self.c2, z2))
                else:
                    # Actual commitment for the first set
                    secret = secrets.get_crypto_data_array()[i].get_crypto_data_array()[j] if secrets else None
                    protocol_commitments.append(protocol.commitment(secret))
            commitments.append(CryptoDataArray(protocol_commitments))
        return CryptoDataArray(commitments)

    def simallcommitment(self, protocol, secret, c2, z2):
        return protocol.simcommitment(secret, c2, z2)

    def determine_proof(self, challenge: int) -> CryptoData:
        self.c1 = (challenge - self.c2) % self.p
        combined_proofs = []
        for i, protocol_set in enumerate(self.protocols):
            protocol_proofs = []
            current_challenge = self.c1 if i == 0 else self.c2
            for j, protocol in enumerate(protocol_set):
                proof_method = protocol.determine_proof if i == 0 else protocol.simdetermine_proof
                protocol_proofs.append(proof_method(current_challenge))
            combined_proofs.append(CryptoDataArray(protocol_proofs))
        return CryptoDataArray(combined_proofs)

    def verify(self, proofs: CryptoData, other_variables: CryptoData) -> bool:
        #Additionally do verfication: challenge = c1 + c2
        result1 = result2 = True
        for i, protocol_set in enumerate(self.protocols):
            for j, protocol in enumerate(protocol_set):
                proof = proofs.get_crypto_data_array()[i].get_crypto_data_array()[j]
                other_variable = other_variables.get_crypto_data_array()[i].get_crypto_data_array()[j]
                verification_result = protocol.verify(proof, other_variable)
                #print(f"Verification result for protocol [{i}][{j}]:", verification_result)
                if verification_result is None:
                    verification_result = False  # Handle None case
                if i == 0:
                    result1 &= verification_result
                else:
                    result2 &= verification_result

        return result1 or result2

    # Unsupported methods
    def simcommitment(self, secrets, c2, z2):
        raise NotImplementedError("Unimplemented method 'simcommitment'")

    def simdetermine_proof(self, challenge):
        raise NotImplementedError("Unimplemented method 'simdetermine_proof'")

    def simverify(self, proofs, other_variables):
        raise NotImplementedError("Unimplemented method 'simverify'")
