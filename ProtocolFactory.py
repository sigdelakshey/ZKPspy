
#WIP
from ZKProtocol import ZKProtocol # type: ignore
from SchnorrProtocolProveSecretKey import SchnorrProtocolProveSecretKey # type: ignore
from PedersenSchnorrProtocol import PedersenSchnorrProtocol # type: ignore
from OrProofProtocol import OrProofProtocol # type: ignore

from Config import ZKConfig

class ProtocolFactory:
    @staticmethod
    def get_protocol(name, config: ZKConfig, sub_protocols=None):
        if name == 'SchnorrSecret':
            return SchnorrProtocolProveSecretKey(config)
        elif name == 'PedersenSchnorr':
            return PedersenSchnorrProtocol(config)
        elif name == 'OrProof':
            if sub_protocols:
                return OrProofProtocol(config, sub_protocols)
            else:
                raise ValueError("OrProof requires a list of sub-protocols")
        raise ValueError("Unknown protocol")
