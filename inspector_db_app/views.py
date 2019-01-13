from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404
from django.template import loader

from inspector_db_app.logic.table import Table, TableDoesNotExist


@login_required
def index(_):
    return HttpResponse("Hello, world. You're at the inspector_db_app index.")


@login_required
def get_table(request, table_name):
    template = loader.get_template('inspector_db_app/table.html')
    try:
        table = Table(table_name)
    except TableDoesNotExist:
        raise Http404("Table {} does't exist".format(table_name))
    context = {
        'column_names': table.get_columns(),
        'records': table.get_records(50)
    }
    return HttpResponse(template.render(context, request))
