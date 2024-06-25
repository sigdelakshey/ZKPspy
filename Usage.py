from CryptoData import BigIntData, CryptoDataArray
from ProtocolFactory import ProtocolFactory
from Config import ZKConfig
from PublicGenerator import PublicGenerator
import logging

logging.basicConfig(level=logging.INFO, format='%(message)s')

def test_pedersen_schnorr_protocol(config, m, r1, challenge):
    try:
        pedersen_schnorr = ProtocolFactory.get_protocol('PedersenSchnorr', config)
        ped_secrets = CryptoDataArray([BigIntData(m), BigIntData(r1)])
        ped_commitments = pedersen_schnorr.commitment(ped_secrets)
        ped_proof = pedersen_schnorr.determine_proof(challenge)
        assert pedersen_schnorr.verify(ped_proof, CryptoDataArray([ped_commitments.get_crypto_data_array()[0], ped_commitments.get_crypto_data_array()[1], BigIntData(challenge)]))
        logging.info("Pedersen Schnorr Protocol Proof Verification: PASS")
    except AssertionError:
        logging.error("Pedersen Schnorr Protocol Proof Verification: FAIL")

def main():
    prime_generator = PublicGenerator()
    #prime_generator.display_parameters()

    config = ZKConfig(p=prime_generator.p, q=prime_generator.q, g=prime_generator.g, h=prime_generator.h, y=prime_generator.y)
    m = 2
    r1 = 3
    x = prime_generator.x  
    challenge = 123456789

    test_pedersen_schnorr_protocol(config, m, r1, challenge)

if __name__ == "__main__":
    main()
