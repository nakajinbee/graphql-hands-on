import strawberry
from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter

# ===========================
# 1️⃣ オブジェクト型(User)を定義
# ===========================
@strawberry.type
class User:
    id: int
    name: str
    age: int


# ===========================
# 2️⃣ Query定義
# ===========================
from typing import Optional

@strawberry.type
class Query:
    @strawberry.field
    def users(self) -> list[User]:
        return [
            User(id=1, name="Alice", age=25),
            User(id=2, name="Bob", age=30),
            User(id=3, name="Charlie", age=22),
        ]

    @strawberry.field
    def user(self, id: int) -> Optional[User]:
        all_users = [
            User(id=1, name="Alice", age=25),
            User(id=2, name="Bob", age=30),
            User(id=3, name="Charlie", age=22),
        ]
        for u in all_users:
            if u.id == id:
                return u
        return None



# ===========================
# 3️⃣ FastAPIアプリ統合
# ===========================
schema = strawberry.Schema(query=Query)
app = FastAPI()
graphql_app = GraphQLRouter(schema)
app.include_router(graphql_app, prefix="/graphql")
