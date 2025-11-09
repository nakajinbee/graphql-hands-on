import strawberry
from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter
from typing import Optional

# ===========================
# 1️⃣ オブジェクト型(User)定義
# ===========================
@strawberry.type
class User:
    id: int
    name: str
    age: int


# ===========================
# 2️⃣ データの保存領域（擬似DB）
# ===========================
# メモリ上で一時的に保持
users_data: list[User] = [
    User(id=1, name="Alice", age=25),
    User(id=2, name="Bob", age=30),
    User(id=3, name="Charlie", age=22),
]


# ===========================
# 3️⃣ Query定義
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
# 4️⃣ Mutation定義
# ===========================
@strawberry.type
class Mutation:
    @strawberry.mutation
    def create_user(self, name: str, age: int) -> User:
        new_id = len(users_data) + 1
        new_user = User(id=new_id, name=name, age=age)
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
# 5️⃣ スキーマとFastAPI統合
# ===========================
schema = strawberry.Schema(query=Query, mutation=Mutation)
app = FastAPI()
graphql_app = GraphQLRouter(schema)
app.include_router(graphql_app, prefix="/graphql")
