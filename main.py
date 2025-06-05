from fastapi import FastAPI, HTTPException, Query
from typing import List,Optional
from uuid import uuid4, UUID

from models import Item, ItemCreate, ItemUpdate, ItemStatus
from utils import generate_product_description
from utils import extract_item_data_from_text  
from models import ItemCreate 
app = FastAPI(title="Inventory Management System with Status Tracking")
from fastapi import Depends, Header
from auth import fake_users_db
from models import User, UserRole

def get_current_user(x_username: str = Header(...)) -> User:
    user = fake_users_db.get(x_username)
    if not user:
        raise HTTPException(status_code=403, detail="Unauthorized user")
    return user

def require_role(required_role: UserRole):
    def role_dependency(user: User = Depends(get_current_user)):
        if user.role != required_role:
            raise HTTPException(status_code=403, detail="Forbidden: insufficient permissions")
        return user
    return role_dependency

inventory = {}


@app.post("/items/", response_model=Item)
def add_item(item: ItemCreate, user: User = Depends(require_role(UserRole.admin))):
    item_data = item.dict()

    # If no description provided, generate one using OpenAI
    if not item_data.get("description"):
        item_data["description"] = generate_product_description(
            name=item_data["name"],
            category=item_data["category"]
        )

    item_id = uuid4()
    new_item = Item(id=item_id, **item_data)
    inventory[item_id] = new_item
    return new_item



@app.put("/items/{item_id}", response_model=Item)
def update_item(item_id: UUID, item: ItemUpdate, user: User = Depends(require_role(UserRole.admin))):
    if item_id not in inventory:
        raise HTTPException(status_code=404, detail="Item not found")
    
    stored_item = inventory[item_id]
    updated_data = item.dict(exclude_unset=True)
    updated_item = stored_item.copy(update=updated_data)
    inventory[item_id] = updated_item
    return updated_item


@app.delete("/items/{item_id}")
def delete_item(item_id: UUID, user: User = Depends(require_role(UserRole.admin))):
    if item_id not in inventory:
        raise HTTPException(status_code=404, detail="Item not found")
    
    del inventory[item_id]
    return {"message": "Item deleted successfully"}


@app.get("/items/", response_model=List[Item])
def list_items():
    return list(inventory.values())

@app.get("/items/search", response_model=List[Item])
def search_items(
    name: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    status: Optional[ItemStatus] = Query(None),
    min_quantity: Optional[int] = Query(None),
    description_contains: Optional[str] = Query(None)
):
    results = list(inventory.values())

    if name:
        results = [item for item in results if name.lower() in item.name.lower()]
    if category:
        results = [item for item in results if category.lower() in item.category.lower()]
    if status:
        results = [item for item in results if item.status == status]
    if min_quantity is not None:
        results = [item for item in results if item.quantity >= min_quantity]
    if description_contains:
        results = [item for item in results if item.description and description_contains.lower() in item.description.lower()]

    return results



@app.post("/items/from-text", response_model=Item)
def add_item_from_text(input_text: str, user: User = Depends(require_role(UserRole.admin))):
    try:
        parsed_data = extract_item_data_from_text(input_text)

        if "description" not in parsed_data or not parsed_data["description"]:
            parsed_data["description"] = generate_product_description(
                name=parsed_data["name"],
                category=parsed_data["category"]
            )


        item_id = uuid4()
        new_item = Item(id=item_id, **parsed_data)
        inventory[item_id] = new_item
        return new_item
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"AI parsing failed: {str(e)}")


