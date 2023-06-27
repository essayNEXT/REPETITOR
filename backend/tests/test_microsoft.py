from repetitor_backend.external_api.microsoft import translate


async def test_microsoft(
        session, src_lng: str = "uk", trg_lng: str = "en", text: str = "додати"
) -> str:
    result = await translate(session, src_lng, trg_lng, text)
    return result
