# chat_project/api/resolvers.py

import uuid
from ariadne import QueryType
from graphql import GraphQLResolveInfo

# from django.contrib import auth
from shop.models import Renter


query = QueryType()

# User = auth.get_user_model()


@query.field("renter")
def resolve_renter(root, info: GraphQLResolveInfo, renter_id):
    renter = Renter.objects.filter(id=renter_id)
    assert renter.exists(), "Renter must've been instantiated"
    return renter.get()


@query.field("renters")
def resolve_renters(root, info: GraphQLResolveInfo):
    return Renter.objects.all()


# @query.field("user")
# def resolve_user(root, info):
#     assert info.context["request"].user.is_authenticated, "User must be authenticated"
#     return info.context["request"].user
#
#
# @query.field("users")
# def resolve_users(root, info):
#     assert info.context["request"].user.is_authenticated, "User must be authenticated"
#     return User.objects.all()
