from dataclasses import dataclass

from app.server import app


@dataclass
class Merchant:
    id: str
    group_id: str
    name: str
    logo: str
    emoji: str
    category: str
    address: str
    postcode: str
    latitude: float
    logitude: float
    suggested_tags: str
    google_place_id: str
    google_place_name: str
    website: str


def build_merchant(data: dict):
    app.logger.debug(f'merchant data={data}')
    address = data.get('address', {})
    metadata = data.get('metadata', {})

    return Merchant(
        data['id'],
        data['group_id'],
        data['name'],
        data['logo'],
        data['emoji'],
        data['category'],
        address.get('formatted'),
        address.get('postcode'),
        address.get('latitude'),
        address.get('longitude'),
        metadata.get('suggested_name'),
        metadata.get('google_places_id'),
        metadata.get('google_places_name'),
        metadata.get('website')
    )