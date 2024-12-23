from ariadne.explorer import ExplorerGraphiQL
from ariadne_django.views import GraphQLView
from django.http import HttpResponse
from django.utils._os import safe_join
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


# import posixpath
# from pathlib import Path
#
# from django.utils._os import safe_join
# from django.views.static import serve as static_serve


def serve_react(request, path, document_root=None):
    path = posixpath.normpath(path).lstrip("/")
    fullpath = Path(safe_join(document_root, path))
    if fullpath.is_file():
        return static_serve(request, path, document_root)
    else:
        return static_serve(request, "index.html", document_root)
