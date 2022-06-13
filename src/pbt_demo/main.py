from typing import List

from fastapi import APIRouter, FastAPI, status
from fastapi.responses import JSONResponse

from pbt_demo.models import Item, ItemUpdate, Message
from pbt_demo.storage import items

app = FastAPI()

router = APIRouter(prefix="/items")


@router.get("/", response_model=List[Item])
async def list_all_items():
    return items


@router.get(
    "/{item_id}",
    response_model=Item,
    responses={status.HTTP_404_NOT_FOUND: {"model": Message}},
)
async def get_item_details(item_id: int):
    try:
        item = next(filter(lambda x: x.id == item_id, items))
    except StopIteration:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"message": f"Item with ID {item_id} not found"},
        )
    return item


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=Item,
    responses={status.HTTP_409_CONFLICT: {"model": Message}},
)
async def save_item(item: Item):
    try:
        existing_item = next(filter(lambda x: x.id == item.id, items))
    except StopIteration:
        items.append(item)
        return item
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={
            "message": f"Cannot create item with ID {existing_item.id}. This item already exists"
        },
    )


@router.put(
    "/{item_id}",
    response_model=Item,
    responses={status.HTTP_404_NOT_FOUND: {"model": Message}},
)
async def update_item(item_id: int, item_update: ItemUpdate):
    try:
        item = next(filter(lambda x: x.id == item_id, items))
    except StopIteration:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"message": f"Item with ID {item_id} not found"},
        )
    for key, value in item_update.dict().items():
        if value is not None:
            setattr(item, key, value)
    return item


@router.delete(
    "/{item_id}",
    response_model=Item,
    responses={status.HTTP_404_NOT_FOUND: {"model": Message}},
)
async def delete_item(item_id: int):
    try:
        item = next(filter(lambda x: x.id == item_id, items))
    except StopIteration:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"message": f"Item with ID {item_id} not found"},
        )
    items.remove(item)
    return item


app.include_router(router)
