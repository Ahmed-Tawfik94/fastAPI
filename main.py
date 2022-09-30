from typing import Union

from fastapi import FastAPI , Query
from pydantic import Required
app = FastAPI()

#Query params and String Validation
# also we can add a default value by passing the value to the default param in the Qurey function
@app.get("/items/")
async def read_items(q: Union[str, None] = Query(default=None ,min_length=3, max_length=50,regex="^fixedquery$")):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results

# we can require the Query string by doing the following
@app.get("/items2/")
async def read_items2(q: str = Query(min_length=3 )):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results

# Required with Ellipsis
@app.get("/items3/")
async def read_items3(q: str = Query(default=..., min_length=3)):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results

# Use Pydantic's Required instead of Ellipsis (...)
@app.get("/items/")
async def read_items(q: str = Query(default=Required, min_length=3)):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results

# Query Paramater list /multiple values
#also we can add defaults to it
# also we can pass list instead of List[str] but it can not check for the types in the list
from typing import List
@app.get("/items_list/")
async def read_items(q: Union[List[str], None] = Query(default=None)):
    query_items = {"q": q}
    return query_items

# what about adding more metadata
# we can add a title to show in our documentation

@app.get("/readers/")
async def read_readers(
    q: Union[str, None] = Query(default=None, title="Query string",
        description="Query string for the items to search in the database that have a good match",
        min_length=3)
    ):
    results = {"readers": [{"reader_id": "Foo"}, {"reader_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results
@app.get("/readers_alias/")
async def read_readers_alias(
    q: Union[str, None] = Query(default=None, title="Query string",
        alias="reader-query",
        description="Query string for the items to search in the database that have a good match",
        min_length=3)
    ):
    results = {"readers": [{"reader_id": "Foo"}, {"reader_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


# Deprecated

@app.get("/posts/")
async def read_posts(
    q: Union[str, None] = Query(
        default=None,
        alias="post-query",
        title="Query string",
        description="Query string for the posts to search in the database that have a good match",
        min_length=3,
        max_length=50,
        regex="^fixedquery$",
        deprecated=True,
    )
):
    results = {"posts": [{"post_id": "Foo"}, {"post_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results

# Exclude from OpenAPI
# To exclude a query parameter from the generated OpenAPI schema (and thus, from the automatic documentation systems),
# set the parameter include_in_schema of Query to False:
# @app.get("/items/")
# async def read_items(
#     hidden_query: Union[str, None] = Query(default=None, include_in_schema=False)
# ):
#     if hidden_query:
#         return {"hidden_query": hidden_query}
#     else:
#         return {"hidden_query": "Not found"}

"""
Recap

You can declare additional validations and metadata for your parameters.

Generic validations and metadata:

alias
title
description
deprecated
Validations specific for strings:

min_length
max_length
regex
In these examples you saw how to declare validations for str values.

See the next chapters to see how to declare validations for other types, like numbers.
"""

# Path Parameter and Numaric Validation

from fastapi import Path
@app.get("/items/{item_id}")
async def read_item(item_id:int = Path(title="the ID of the item to get"),
        q:Union[str,None]=Query(default=None, alias="item-query")):
    results={"item_id":item_id}
    if q:
        results.update({"q":q})
    return q

# pass * if you want to change order
"""
If you want to declare the q query parameter without a Query nor any default value,
and the path parameter item_id using Path
, and have them in a different order, Python has a little special syntax for that.
Pass *, as the first parameter of the function.
Python won't do anything with that *, 
but it will know that all the following parameters should be called as keyword arguments 
(key-value pairs), also known as kwargs. Even if they don't have a default value.
"""
@app.get("/items/{item_id}")
async def read_items(q: str, item_id: int = Path(title="The ID of the item to get")):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results

# Number validation: greater than or equal
"""
 similar to the example below 
 we can use 
 gt: greater than
 lt: less than
 le: less than or equal
 ge: greater than or equal
"""
@app.get("/items1/{item_id}")
async def read_items1(*,item_id:int=Path(title="The ID of the item to get",gt=1),q:str):
    results={"item_id":item_id}
    if q:
        results.update({"q":q})
    return results

# Body - multiple Parameter

from pydantic import BaseModel

class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None


@app.put("/items/{item_id}")
async def update_item(
    *,
    item_id: int = Path(title="The ID of the item to get", ge=0, le=1000),
    q: Union[str, None] = None,
    item: Union[Item, None] = None,
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    if item:
        results.update({"item": item})
    return results

class User(BaseModel):
    username: str
    full_name: Union[str, None] = None


@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item, user: User):
    results = {"item_id": item_id, "item": item, "user": user}
    return results


# Singular values in body
"""
if decided to extend the previous modle by adding another key 'foo' in the same body 
by default FastAPI will treat it as a query parameter. 
but there is a way to instruct FastAPI to treat it as another body key using Body():
"""
from fastapi import Body

@app.get('/singular/{item_id}')
async def singular_value(item_id:int, item:Item,user:User,foo:int =Body()):
    results= {
        "item_id":item_id,
        "item":item,
        "user":user,
        "foo":foo
    }
    return results