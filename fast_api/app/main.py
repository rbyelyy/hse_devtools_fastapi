from __future__ import annotations

from fastapi import FastAPI, HTTPException
from enum import Enum
from pydantic import BaseModel, ValidationError

app = FastAPI()
class DogType(str, Enum):
    terrier = "terrier"
    bulldog = "bulldog"
    dalmatian = "dalmatian"


class Dog(BaseModel):
    name: str
    pk: int
    kind: DogType


class Timestamp(BaseModel):
    id: int
    timestamp: int

dogs_db = {
    0: Dog(name='Bob', pk=0, kind='terrier'),
    1: Dog(name='Marli', pk=1, kind="bulldog"),
    2: Dog(name='Snoopy', pk=2, kind='dalmatian'),
    3: Dog(name='Rex', pk=3, kind='dalmatian'),
    4: Dog(name='Pongo', pk=4, kind='dalmatian'),
    5: Dog(name='Tillman', pk=5, kind='bulldog'),
    6: Dog(name='Uga', pk=6, kind='bulldog')
}

post_db = [
    Timestamp(id=0, timestamp=12),
    Timestamp(id=1, timestamp=10)
]

@app.get('/')
def root():
    """
    Welcome message for Dog Clinic API
    :return: welcome string in dict
    """
    return "Dog Clinic API!"

@app.get("/post", response_model=Timestamp)
async def get_post():
    """
    Get record from the post db based (*** only 0 according to swagger docs)
    :return: record from the post database
    """
    return post_db[0]

@app.get("/dog")
async def get_dogs(kind: DogType):
    """
    Get all dogs based on the kind parameter
    :param kind: type of the dog
    :return: all dogs based on the kind
    """
    return {k: v for k, v in dogs_db.items() if v.kind == kind}

@app.get("/dog/{pk}")
async def get_dogs(pk: int):
    """
    Get a dog from db based on the pk provided
    :param pk:a primary key
    :return: dog based on the given pk
    """
    if pk not in dogs_db.keys():
        raise HTTPException(status_code=404, detail=f"{pk} is not found")
    return {k: v for k, v in dogs_db.items() if v.pk == pk}

@app.patch("/dog/{pk}", response_model=Dog)
async def update_dog_by_pk(pk: int, dog: Dog):
    """
    Update dog record in memory db
    :param pk: a primary key
    :param dog: dog to update
    :return: a dog object
    """
    if dog.pk != pk:
        raise HTTPException(status_code=404, detail=f"URL {pk} is not equal to body {dog.pk}")
    try:
        dogs_db[dog.pk] = dog
    except ValidationError as e:
        print(e)
    return dogs_db[dog.pk]

@app.post("/dog", response_model=Dog)
async def create_dog(dog: Dog):
    """
    Create a new record in the dog database
    :param dog: a dog object
    :return: newly created dog object
    """
    try:
        if dog.pk in [v.pk for k, v in dogs_db.items()]:
            raise HTTPException(status_code=400, detail=f"{dog.pk} already exists")
        dogs_db[dog.pk] = dog
    except ValidationError as e:
        print(e)
    return dog