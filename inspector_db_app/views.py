from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404
from django.template import loader

from inspector_db_app.logic.table import Table, TableDoesNotExist
from inspector_db_app.logic.tables import Tables


@login_required
def table_index(request):
    template = loader.get_template('inspector_db_app/table_index.html')
    tables = Tables()
    context = {
        'table_names': tables.get_public_tables()
    }
    return HttpResponse(template.render(context, request))


@login_required
def get_table(request, table_name):
    template = loader.get_template('inspector_db_app/table.html')
    try:
        table = Table(table_name)
    except TableDoesNotExist:
        raise Http404("Table {} does't exist".format(table_name))
    tables = Tables()
    context = {
        'column_names': table.get_columns(),
        'records': table.get_records(50),
        'table_names': tables.get_public_tables(),
        'current_table_name': table_name,
    }
    return HttpResponse(template.render(context, request))
