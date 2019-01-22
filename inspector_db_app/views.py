from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404
from django.template import loader

from inspector_db_app.logic.utils.logger_utils import get_logger
from inspector_db_app.logic.db.query import Query
from inspector_db_app.logic.db.table import Table, TableDoesNotExist
from inspector_db_app.logic.db.tables import Tables

logger = get_logger(__name__)


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
    context = _get_table_context(table, tables)
    return HttpResponse(template.render(context, request))


@login_required
def execute_query(request):
    raw_query = request.GET.get('query')
    query = Query(raw_query)
    context = {
        'query_title': raw_query,
        'column_names': query.get_column_names(),
        'records': query.get_records()
    }
    template = loader.get_template('inspector_db_app/query.html')
    return HttpResponse(template.render(context, request))


def _get_table_context(table, tables):
    return {
        'column_names': table.get_columns(),
        'records': table.get_all_records(),
        'table_names': tables.get_public_tables(),
        'current_table_name': table.table_name,
        'table_title': 'All',
    }
