import uuid


def generate_prefixed_uuid(prefix: str, length: int | None = None) -> str:
    uid = str(uuid.uuid4().hex)
    full_id = f"{prefix}-{uid}"

    if length is not None:
        return full_id[:length]
    return full_id
