from typing import Optional
from fastapi import FastAPI, Response, status
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

my_posts = [{"title": "Post 1", "content": "This is my first post", "id": 1}, {"title": "Post 2", "content": "This is my second post", "id": 2}]

def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/posts")
def get_posts():
    return {"data": "Your posts"}

# stored as pydantic model
@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    post_dict = post.dict()
    post_dict["id"] = randrange(0,1000000)
    my_posts.append(post_dict)

    return {"data": post_dict}

# id field is a path parameter
@app.get("/posts/{id}")
def get_post(id: int, response: Response):
    print(id)
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=404, detail=f"Post with id {id} not found")
        return {'message': f"Post with id {id} not found"}
    return {"post_detail":post}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    post = find_post(id)
    if not post:
        return HTTPException(status_code=404, detail=f"Post with id {id} not found")

    my_posts.remove(post)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    post = find_post(id)
    if not post:
        return HTTPException(status_code=404, detail=f"Post with id {id} not found")

    post.update(post.dict())
    return {"data": post}

