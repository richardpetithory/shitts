import os

from ariadne import make_executable_schema, load_schema_from_path

from .directives import directives
from .resolvers.shop import query as shop_queries
from .scalars import scalars

type_defs_path = os.path.join(os.path.dirname(__file__), "schema")
type_defs = load_schema_from_path(type_defs_path)

queries = [shop_queries] + scalars

schema = make_executable_schema(type_defs, queries, directives=directives)
