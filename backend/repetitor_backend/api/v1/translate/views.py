from typing import List, Annotated
from uuid import UUID
from fastapi import APIRouter, Query

from repetitor_backend import tables
from .serializers import (
    ItemCreateRequest,
    ItemResponse,
    REGEX_PATH,
    UpdateItemRequest,
)
from repetitor_backend.db.crud import item, question, right_answ_item, item_relation
import logging
from repetitor_backend import tables
from repetitor_backend.external_api.microsoft import translate

logger = logging.getLogger()

router = APIRouter()


# @router.post("/translate/")
# async def create_item(new_item: ItemCreateRequest) -> UUID | str:
#
#     return await item.create(**new_item.dict())


@router.get(
    "/creating_phrases/",
    # response_model=List[ItemResponse],
    # response_model_exclude_none=True,
    # response_model_exclude={"is_active"},
)
async def creating_phrases(
    source_text: str,
    author: UUID | None,
    context_1: UUID | None,
    context_2: UUID | None,
    explanation: UUID | None = "95dd33a8-a6f6-410e-8456-46a6b140f8cc",
    type: UUID | None = "63442faf-9bb1-42ab-a8c8-320bb72d5d72",
    is_active: bool = True,
    # item__context__name_short: Annotated[
    #     str | None, Query(min_length=2, max_length=10)
    # ],
    # item__context__name_short_2: Annotated[
    #     str | None, Query(min_length=2, max_length=10)
    # ],
) -> list:
    pass
    from repetitor_backend.app import app
    target_text = await translate(session=app.session, source_lng="en", target_lng="uk", text=source_text)
    target_text_2 = await translate(session=app.session, source_lng="uk", target_lng="en", text=source_text)
    return [dict(text=source_text, target_text=target_text, target_text_2=target_text_2)]
    create_item_relation = await item_relation.create(
        author=author,
        explanation=explanation,
        type=type,
    )
    create_item_for_question = await item.create(
        author=author,
        context=context_1,
        text=source_text,
    )
    from repetitor_backend.app import app
    target_text = await translate(session=app.session, source_lng="en", target_lng="uk", text=source_text)
    "function translate"  # !!!!!!!!!!!!!!!

    create_item_for_right_answ_item = await item.create(
        author=author,
        context=context_2,
        text=target_text,
    )
    create_question = await question.create(
        relation=create_item_relation,
        item=create_item_for_question,
    )
    create_right_answ_item = await right_answ_item.create(
        relation=create_item_relation,
        item=create_item_for_right_answ_item,
    )

    return [
        {
            "status": 200,
            "result": "вроді все норм",
            # "context": f"{item__context__name_short} & {item__context__name_short_2} ",
            # "source_word": item__text,
            # "target_word": result_4[0]["text"]
        }
    ]


######################


@router.get(
    "/translate/",
    # response_model=List[ItemResponse],
    # response_model_exclude_none=True,
    # response_model_exclude={"is_active"},
)
async def get_translate(
    item__text: str,
    item__author: UUID,
    item__context__name_short: Annotated[str, Query(min_length=2, max_length=10)],
    item__context__name_short_2: Annotated[str, Query(min_length=2, max_length=10)],
    is_active: bool = True,
) -> list:
    """
    Get a list of existing item according to match conditions:

    Parameters:
    - id: UUID of item
    - item__text: str, max lenght is 255 symbols - data description
    - image: str, max lenght is 255 symbols - link to associative picture
    - sound: str, max lenght is 255 symbols - link to associative sound
    - author: UUID of customer, used for ForeignKey links with Customer
    - context: UUID of context, used for ForeignKey links with Context
    - is_key_only: bool - as a result, return:
        - only the ID of the item object;
        - return all object parameters

    Return:
    - List that contains the results of the query
    """

    # result = await question.get(
    #     item__author=item__author,
    #     item__text=item__text,
    #     item__context__name_short=item__context__name_short, # uk
    #     is_active=is_active,
    # )
    #
    # if not result:
    #     return [{"status": 404, "step": 1}]
    # uuid_relation: UUID | None = (
    #     result[0].relation if result else None
    # )  # None = нема такого слова, треба створювати
    #
    # result_2 = await right_answ_item.get(
    #     item__author=item__author,
    #     relation=uuid_relation,
    #     item__context__name_short=item__context__name_short_2, # en
    # )
    # if not result_2:
    #     return [{"status": 404, "step": 2}]
    #
    # result_3 = await tables.Item.objects().where(tables.Item.id == result_2[0].item)

    sql_query = f"""
            SELECT i."text"
            FROM item i
            JOIN right_answ_item rai ON rai.item = i.id
            JOIN question q ON q.relation = rai.relation
            JOIN item i2 ON i2.id = q.item
            JOIN context c ON (i2.context = c.id AND  c.name_short IN ('{item__context__name_short}', '{item__context__name_short_2}'))
            WHERE i2."text" = '{item__text}' AND i2.author = '{item__author}';
    """

    sql_query_2 = f"""
        SELECT i."text", ir.id, i.author 
        FROM item i
        LEFT JOIN question q ON q.item = i.id
        LEFT JOIN right_answ_item rai ON rai.item = i.id
        LEFT JOIN item_relation ir ON ir.id = COALESCE(q.relation, rai.relation)
        JOIN context c ON (i.context = c.id AND  c.name_short IN ('{item__context__name_short}', '{item__context__name_short_2}'))
        WHERE i."text" = '{item__text}' AND i.author = '{item__author}' OR 
                ir.id IN (
               SELECT ir2.id
               FROM item i2
               LEFT JOIN question q2 ON q2.item = i2.id
               LEFT JOIN right_answ_item rai2 ON rai2.item = i2.id
               LEFT JOIN item_relation ir2 ON ir2.id = COALESCE(q2.relation, rai2.relation)
               JOIN context c2 ON (i2.context = c2.id AND  c2.name_short IN ('{item__context__name_short}', '{item__context__name_short_2}'))
               WHERE i2."text" = '{item__text}' AND i2.author = '{item__author}'
           ) 
          ;
    """

    result_4 = await tables.Item.raw(sql_query_2).run()
    1 == 1

    # блок аналізу  результату
    #
    fin_result = [
        {
            "status": 200,
            "result": "пошук не дав результату. Такого слова не має в БД",
        }
    ]

    if len(result_4) == 1:
        fin_result = [
            {
                "status": 200,
                "result": "слово є, проте не має перекладу в даному контексті",
            }
        ]
    else:
        result_4 = [
            item for item in result_4 if item.get("text") != item__text
        ]  # видаляємо source-слово
        if len(result_4) == 1:
            fin_result = [
                {
                    "status": 200,
                    "result": "слово є, має 1 переклад в даному контексті",
                    "context": f"{item__context__name_short} & {item__context__name_short_2} ",
                    "source_word": item__text,
                    "target_word": result_4[0]["text"],
                }
            ]
        if len(result_4) > 2:
            fin_result = [
                {
                    "status": 200,
                    "result": "ГЛЮК!!. слово є, має декілька перекладів в даному контексті",
                    "context": f"{item__context__name_short} & {item__context__name_short_2} ",
                    "source_word": item__text,
                    "target_word": [item["text"] for item in result_4],
                }
            ]

        # return [
        #     {
        #         "status": 200,
        #         "context": f"{item__context__name_short} & {item__context__name_short_2} ",
        #         "source_word": item__text,
        #         "target_word": result_4[0]["text"],
        #     }
        # ]

    # fin_result = results
    return fin_result


#
# @router.patch("/translate/")
# async def update_item(update_item: UpdateItemRequest) -> UUID | None:
#     """
#     Update existing record in customer context.
#
#     Parameters:
#     - id: UUID of customer context, required
#     - text: str, max lenght is 255 symbols - data description
#     - image: str, max lenght is 255 symbols - link to associative picture
#     - sound: str, max lenght is 255 symbols - link to associative sound
#     - author: UUID of customer, used for ForeignKey links with Customer
#     - context: UUID of context, used for ForeignKey links with Context
#
#     Return:
#     - CustomerContext.id: UUID - primary key for new customer context record - UUID type
#     - If there is no record with this id, it returns None
#     """
#
#     return await item.update(**update_item.dict())
#
#
# @router.delete("/translate/")
# async def delete_item(id: UUID) -> UUID | None:
#     """
#     Delete item with item.id == id.
#
#     Parameter:
#     - id - UUID.
#
#     Result:
#     - primary key for deleted record - UUID type.
#     - If there is no record with this id, it returns None.
#
#     If parameter has wrong type - raise TypeError.
#     """
#
#     return await item.delete(id)
