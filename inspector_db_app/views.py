import psycopg2
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404
from django.template import loader

from inspector_db_app.logic.logger_utils import get_logger
from inspector_db_app.logic.table import Table, TableDoesNotExist
from inspector_db_app.logic.tables import Tables

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
    if 'query' in request.GET:
        context = _get_query_context(request.GET['query'], table, tables)
    else:
        context = _get_table_context(table, tables)
    return HttpResponse(template.render(context, request))


def _get_query_context(query, table, tables):
    table_title = query
    try:
        records = table.execute_query(query)
    except psycopg2.ProgrammingError:
        table_title = 'Illegal query: {}'.format(query)
        logger.exception(table_title)
        records = table.get_all_records()
    return {
        'column_names': table.get_columns(),
        'records': records,
        'table_names': tables.get_public_tables(),
        'current_table_name': table.table_name,
        'table_title': table_title,
    }


def _get_table_context(table, tables):
    return {
        'column_names': table.get_columns(),
        'records': table.get_all_records(),
        'table_names': tables.get_public_tables(),
        'current_table_name': table.table_name,
        'table_title': 'All',
    }
