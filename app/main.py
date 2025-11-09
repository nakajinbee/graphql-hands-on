import strawberry
from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter

# ===========================
# 1️⃣ Query定義
# ===========================
@strawberry.type
class Query:
    @strawberry.field
    def hello(self, name: str = "World") -> str:
        """
        name引数を受け取り、挨拶メッセージを返す。
        引数が指定されなければデフォルトで 'World'。
        """
        return f"Hello, {name}! from GraphQL + FastAPI"


# ===========================
# 2️⃣ スキーマとアプリ作成
# ===========================
schema = strawberry.Schema(query=Query)
app = FastAPI()
graphql_app = GraphQLRouter(schema)
app.include_router(graphql_app, prefix="/graphql")
