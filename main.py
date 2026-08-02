from fastapi import FastAPI, HTTPException

from database import (
    create_farm_table,
    get_farm_by_id,
    get_farms,
    insert_farm,
    update_farm,
)
from models import Farm, FarmUpdate

app = FastAPI()
create_farm_table()


# Routes below
@app.get("/")
async def root():
    return {"message": "It's working"}


@app.post("/farms")
async def create_farm(farm: Farm):
    new_id = insert_farm(farm)
    return {"id": new_id, "farm": farm}


@app.get("/farms")
async def get_all_farms():
    all_farms = get_farms()
    return {"Farms": all_farms}


@app.get("/farms/{farm_id}")
async def get_farm(farm_id: int):
    farm = get_farm_by_id(farm_id)
    if farm is None:
        raise HTTPException(status_code=404, detail="Farm not found")
    return {"id": farm_id, "farm": farm}


@app.patch("/farms/{farm_id}")
async def patch_farm(farm_id: int, updates: FarmUpdate):
    updates_dict = updates.model_dump(exclude_unset=True)
    success = update_farm(farm_id, updates_dict)
    if not success:
        raise HTTPException(status_code=404, detail="Farm not found")
    updated_farm = get_farm_by_id(farm_id)
    return {"message": "Farm updated.", "Farm": updated_farm}
