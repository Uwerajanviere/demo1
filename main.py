"""
FastAPI Backend Application
A simple REST API with basic CRUD operations for demonstration.
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import uvicorn

# Initialize FastAPI application
app = FastAPI(
    title="Simple FastAPI Backend",
    description="A basic REST API for demonstration purposes",
    version="1.0.0"
)

# Pydantic model for data validation
class Item(BaseModel):
    """Item model representing a resource in our API"""
    id: Optional[int] = None
    name: str
    description: str
    price: float
    
    class Config:
        """Pydantic configuration for JSON serialization"""
        json_schema_extra = {
            "example": {
                "id": 1,
                "name": "Sample Item",
                "description": "This is a sample item",
                "price": 99.99
            }
        }

# In-memory storage (for demonstration purposes)
items_db: List[Item] = []
next_id = 1

@app.get("/")
async def root():
    """
    Root endpoint that returns a welcome message
    
    Returns:
        dict: A simple welcome message
    """
    return {"message": "Welcome to FastAPI Backend!", "docs": "/docs"}

@app.get("/health")
async def health_check():
    """
    Health check endpoint for monitoring
    
    Returns:
        dict: Health status of the application
    """
    return {"status": "healthy", "version": "1.0.0"}

@app.get("/items", response_model=List[Item])
async def get_items():
    """
    Get all items from the database
    
    Returns:
        List[Item]: List of all items
    """
    return items_db

@app.get("/items/{item_id}", response_model=Item)
async def get_item(item_id: int):
    """
    Get a specific item by ID
    
    Args:
        item_id (int): The ID of the item to retrieve
        
    Returns:
        Item: The requested item
        
    Raises:
        HTTPException: If item is not found
    """
    item = next((item for item in items_db if item.id == item_id), None)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@app.post("/items", response_model=Item)
async def create_item(item: Item):
    """
    Create a new item
    
    Args:
        item (Item): The item data to create
        
    Returns:
        Item: The created item with assigned ID
    """
    global next_id
    item.id = next_id
    next_id += 1
    items_db.append(item)
    return item

@app.put("/items/{item_id}", response_model=Item)
async def update_item(item_id: int, item: Item):
    """
    Update an existing item
    
    Args:
        item_id (int): The ID of the item to update
        item (Item): The updated item data
        
    Returns:
        Item: The updated item
        
    Raises:
        HTTPException: If item is not found
    """
    index = next((i for i, existing_item in enumerate(items_db) if existing_item.id == item_id), None)
    if index is None:
        raise HTTPException(status_code=404, detail="Item not found")
    
    item.id = item_id
    items_db[index] = item
    return item

@app.delete("/items/{item_id}")
async def delete_item(item_id: int):
    """
    Delete an item by ID
    
    Args:
        item_id (int): The ID of the item to delete
        
    Returns:
        dict: Success message
        
    Raises:
        HTTPException: If item is not found
    """
    index = next((i for i, item in enumerate(items_db) if item.id == item_id), None)
    if index is None:
        raise HTTPException(status_code=404, detail="Item not found")
    
    items_db.pop(index)
    return {"message": f"Item {item_id} deleted successfully"}

# Run the application when this file is executed directly
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
