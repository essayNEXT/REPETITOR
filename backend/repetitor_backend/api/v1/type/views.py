import logging
from tests.test_ms_lng_list import get_lng_list
from tests.test_microsoft import test_microsoft
from typing import List
from uuid import UUID
from fastapi import APIRouter


from .serializers import (
    CustomerTypeCreateRequest,
    CustomerTypeResponse,
    ContextTypeCreateRequest,
    ContextTypeResponse,
)
from repetitor_backend.db.crud import contexttype, customertype


logger = logging.getLogger()

router = APIRouter()


@router.post("/type/customer/")
async def create_customer_type(new_customer_type: CustomerTypeCreateRequest) -> UUID:
    """Create a new type of customer.

    Parameters:
    - name: str, max lenght is 50 symbols, required
    - describe: str, max lenght is 200 symbols, required
    """
    return await customertype.create_new_customer_type(
        name=new_customer_type.name, description=new_customer_type.description
    )


@router.get("/type/customer/")
async def get_customer_type(
    id: UUID | None = None,
    name: str | None = None,
    description: str | None = None,
    is_active: bool = True,
) -> List[CustomerTypeResponse]:
    """Get list of Customer Type according of "query" parameter.

    id: UUID, corresponds to the parameter tables.CustomerType.id
    name: str, corresponds to the parameter tables.CustomerType.name
    description: str, corresponds to the parameter tables.CustomerType.description
    is_active: bool, corresponds to the parameter tables.CustomerType.is_active

    Returns a list that contains the results of the query, serialized to
    the CustomerTypeResponce type, constructed as follows:
    SELECT *
    FROM customer_type
    WHERE
            customer_type.id = id
        AND customer_type.name = name
        AND customer_type.description LIKE '%description%'
        AND customer_type.is_active = is_active;

    if some parameter is None (as id, name, description) - the corresponding line
    in the request is simply missing
    """
    results = await customertype.get_customer_type(
        id=id, name=name, description=description, is_active=is_active
    )
    return [CustomerTypeResponse.from_DB_model(db_model=result) for result in results]


@router.post("/type/context/")
async def create_context_type(new_context_type: ContextTypeCreateRequest) -> UUID:
    """Create a new type of context.

    Parameters:
    - name: str, max lenght is 50 symbols, required
    - describe: str, max lenght is 200 symbols, required
    """
    return await contexttype.create(
        name=new_context_type.name, description=new_context_type.description
    )


@router.get("/type/context/")
async def get_context_type(
    id: UUID | None = None,
    name: str | None = None,
    description: str | None = None,
    is_active: bool = True,
) -> List[ContextTypeResponse]:
    """Get list of Context Type according of "query" parameter.

    id: UUID, corresponds to the parameter tables.ContextType.id
    name: str, corresponds to the parameter tables.ContextType.name
    description: str, corresponds to the parameter tables.ContextType.description
    is_active: bool, corresponds to the parameter tables.ContextType.is_active

    Returns a list that contains the results of the query, serialized to
    the CustomerTypeResponce type, constructed as follows:
    SELECT *
    FROM customer_type
    WHERE
            customer_type.id = id
        AND customer_type.name = name
        AND customer_type.describe LIKE '%describe%'
        AND customer_type.is_active = is_active;

    if some parameter is None (as id, name, describe) - the corresponding line
    in the request is simply missing
    """
    results = await contexttype.get(
        id=id, name=name, description=description, is_active=is_active
    )
    return [ContextTypeResponse.from_DB_model(db_model=result) for result in results]


@router.get("/type/ms_lng_list/")
async def ms_lng_list() -> list:
    """Отримує список мов, які зараз підтримуються операціями Перекладача."""
    from repetitor_backend.app import app
    result = await get_lng_list(app.session, "en")
    return result


@router.get("/type/ms_translate/")
async def ms_translate(
        src_lng: str = "uk", trg_lng: str = "en", text: str = "додати"
) -> str:
    """
    The function returns the translation of the entered text, in addition,
    it compares the resulting translation with:
    1. by reverse translation or
    2. with the translation "auto-detecting input language"
        (additional option, not used yet)
       and decides on the correctness of the translation.
    Used Microsoft Azure Cognitive Services Translator REST APIs

    :param source_lang: language from which the translation is carried out
    :param target_lang: language into which the translation is carried out
    :param text: text to be translated
    :return: if the translation is correct, then returns the translation of the input text
    """

    from repetitor_backend.app import app

    result = await test_microsoft(app.session, src_lng, trg_lng, text)
    return result
