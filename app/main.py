import strawberry
from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter
from typing import Optional

# ===========================
# 1️⃣ オブジェクト型定義
# ===========================
@strawberry.type
class Post:
    id: int
    title: str
    content: str
    user_id: int

@strawberry.type
class User:
    id: int
    name: str
    age: int

    @strawberry.field
    def posts(self) -> list[Post]:
        return [p for p in posts_data if p.user_id == self.id]


# ===========================
# 入力型定義
# ===========================
@strawberry.input
class UserInput:
    name: str
    age: int


# ===========================
# 擬似DB（ユーザー）
# ===========================
users_data: list[User] = [
    User(id=1, name="Alice", age=25),
    User(id=2, name="Bob", age=30),
]

# ===========================
# 擬似DB（投稿）
# ===========================
posts_data: list[Post] = [
    Post(id=1, title="Hello GraphQL", content="GraphQL is great!", user_id=1),
    Post(id=2, title="My Second Post", content="FastAPI works well with Strawberry", user_id=2),
]

# ===========================
# 3️ Query定義
# ===========================
@strawberry.type
class Query:
    @strawberry.field
    def users(self) -> list[User]:
        return users_data

    @strawberry.field
    def user(self, id: int) -> Optional[User]:
        for u in users_data:
            if u.id == id:
                return u
        return None


# ===========================
# Mutation定義
# ===========================
@strawberry.type
class Mutation:
    @strawberry.mutation
    def create_user(self, input: UserInput) -> User:
        new_id = len(users_data) + 1
        new_user = User(id=new_id, name=input.name, age=input.age)
        users_data.append(new_user)
        return new_user

    @strawberry.mutation
    def update_user(self, id: int, name: Optional[str] = None, age: Optional[int] = None) -> Optional[User]:
        """id指定でユーザー情報を更新"""
        for u in users_data:
            if u.id == id:
                if name is not None:
                    u.name = name
                if age is not None:
                    u.age = age
                return u
        return None

    @strawberry.mutation
    def delete_user(self, id: int) -> bool:
        """id指定でユーザーを削除"""
        global users_data
        before = len(users_data)
        users_data = [u for u in users_data if u.id != id]
        return len(users_data) < before


# ===========================
# スキーマとFastAPI統合
# ===========================
schema = strawberry.Schema(query=Query, mutation=Mutation)
app = FastAPI()
graphql_app = GraphQLRouter(schema)
app.include_router(graphql_app, prefix="/graphql")
