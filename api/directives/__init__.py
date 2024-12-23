from ariadne import SchemaDirectiveVisitor
from graphql import GraphQLResolveInfo, GraphQLError, GraphQLField


class IsAuthenticated(SchemaDirectiveVisitor):
    def visit_field_definition(self, field, object_type) -> GraphQLField:
        original_resolver = field.resolve

        def resolver(obj, info: GraphQLResolveInfo, **kwargs):
            request = info.context["request"]
            if not request.user.is_authenticated:
                raise GraphQLError("unauthorized")

            if original_resolver is None:
                raise Exception(
                    "Ooops.. cannot find resolver, is it registered in schema?"
                )

            return original_resolver(obj, info, **kwargs)

        field.resolve = resolver
        return field


directives = {
    "isAuthenticated": IsAuthenticated,
}
