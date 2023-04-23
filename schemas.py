from typing import List, Optional
from pydantic import BaseModel


class Direction(BaseModel):
    step: int
    instruction: str


class RatingCreate(BaseModel):
    grade: int


class RecipeBase(BaseModel):
    title: str
    description: str
    ingredients: List[str]
    guide: List[Direction]
    total_time: int
    photo: Optional[bytes] = None


class RecipeCreate(RecipeBase):
    pass


class Recipe(RecipeBase):
    id: int
    rating: Optional[float] = None
    author_id: int

    class Config:
        orm_mode = True


class User(BaseModel):
    id: int
    email: str
    full_name: Optional[str] = None
    disabled: Optional[bool] = None

    class Config:
        orm_mode = True


class RecipeList(BaseModel):
    recipes: List[Recipe]


class RecipeUpdate(BaseModel):
    title: Optional[str]
    description: Optional[str]
    ingredients: Optional[List[str]]
    guide: Optional[List[str]]
    total_time: Optional[int]
    photo: Optional[bytes]