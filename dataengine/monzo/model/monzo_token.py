import json
from dataclasses import dataclass
from common.dataclass_json_encoder import DataclassJsonEncoder
from common.util import current_time_sec


@dataclass
class MonzoToken:
    access_token: str
    client_id: str
    expires_in_sec: int
    refresh_token: str
    token_type: str
    user_id: str
    account_id: str
    created_at_sec: str = current_time_sec()

    def to_json(self):
        return json.dumps(self, cls=DataclassJsonEncoder)

    @staticmethod
    def from_json(data):
        return MonzoToken(**json.loads(data))
