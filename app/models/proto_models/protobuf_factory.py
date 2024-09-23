from .titanium_pb2 import NetworkCredentials, NetworkInformation, BrokerConfig

class ProtobufFactory:
    def __init__(self, payload_dict:dict = None):
        self._payload_dict = payload_dict
        
        self._protobufs_dict = {
            0: NetworkCredentials,
            1: NetworkInformation,
            2: BrokerConfig,
        }

    def load_config_from_json(self, memory_area):
        protobuf = self._protobufs_dict.get(memory_area)()
        
        if self._payload_dict is not None:
            for key, value in self._payload_dict.items():
                setattr(protobuf, key, value)
        
        return protobuf