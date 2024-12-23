from ariadne.explorer import ExplorerGraphiQL
from ariadne_django.views import GraphQLView
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from .schema import schema


@csrf_exempt
def graphql_view(request):
    if request.method == "GET":
        explorer = ExplorerGraphiQL()
        return HttpResponse(explorer.html({"request": request}))

    return GraphQLView.as_view(
        schema=schema,
        introspection=True,
    )(request)
