from fastapi import FastAPI, Depends, HTTPException
import schemas

from db_connection import Session, get_db
from func.facecontrol import authenticate_user, User_new, UserCreate, get_user_by_email, get_password_hash, get_current_user
from models.recipe_models import Recipe
from models.user_models import User

app = FastAPI()


@app.post("/api/token/")
async def login_for_access_token(email: str, password: str):
    return authenticate_user(email, password)


@app.post("/api/register", response_model=User_new)
def register(user: UserCreate, db: Session = Depends(get_db)):
    db_user = get_user_by_email(user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = get_password_hash(user.password)
    db_user = User(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@app.post("/recipes", response_model=schemas.Recipe)
def create_recipe(recipe: schemas.RecipeCreate, db: Session = Depends(get_db),
                  current_user: User = Depends(get_current_user)):
    title = recipe.title
    description = recipe.description
    ingredients = recipe.ingredients
    guide = recipe.guide
    photo = recipe.photo

    # Создаем список Direction из guide
    directions = []
    total_time = 0
    for d in guide:
        direction = schemas.Direction(description=d[0], time=d[2], photo=d[3])
        directions.append(direction)
        total_time += d[2]
    new_recipe = Recipe(title=title, description=description,
                         ingredients=ingredients, guide=directions,
                         total_time=total_time, author_id=current_user.id, photo=photo)

    db.add(new_recipe)
    db.commit()
    db.refresh(new_recipe)

    return new_recipe


@app.get("/recipes/{recipe_id}", response_model=Recipe)
def read_recipe(recipe_id: int, db: Session = Depends(get_db)):
    recipe = db.query(Recipe).filter(Recipe.id == recipe_id).first()
    if recipe is None:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return recipe


@app.get("/recipes", response_model=schemas.RecipeList)
def read_recipes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    recipes = db.query(Recipe).offset(skip).limit(limit).all()
    return recipes


@app.put("/recipes/{recipe_id}")
def update_recipe(recipe_id: int, recipe: schemas.RecipeUpdate, db: Session = Depends(get_db)):
    db_recipe = db.query(Recipe).filter(Recipe.id == recipe_id).first()

    if not db_recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")

    db_recipe.title = recipe.title
    db_recipe.description = recipe.description
    db_recipe.ingredients = recipe.ingredients
    db_recipe.guide = recipe.guide
    db_recipe.total_time = recipe.total_time
    db_recipe.photo = recipe.photo

    db.commit()

    return db_recipe
