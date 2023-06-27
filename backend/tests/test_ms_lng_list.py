from repetitor_backend.external_api.microsoft import translate_lng


async def get_lng_list(session, lng: str = "en") -> list:
    result = await translate_lng(session, lng)

    # список підтримуваних мов
    res = [key for key in result]
    # return {len(res): res} -> dict
    return res  # list
