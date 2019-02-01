from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404, HttpResponseBadRequest
from django.template import loader

from app.logic.db.db import Db
from app.logic.db.query import Query, QueryExecutionError
from app.logic.db.table import Table, TableDoesNotExist
from app.logic.utils.logger_utils import get_logger

logger = get_logger(__name__)


@login_required
def table_index(request):
    db_name = request.user.username
    template = loader.get_template('app/table_index.html')
    tables = Db(db_name)
    context = {
        'table_names': tables.get_public_tables()
    }
    return HttpResponse(template.render(context, request))


@login_required
def get_table(request, table_name):
    db_name = request.user.username
    template = loader.get_template('app/table.html')
    try:
        table = Table(db_name, table_name)
    except TableDoesNotExist:
        raise Http404("Table {} does't exist".format(table_name))
    db = Db(db_name)
    context = _get_table_context(table, db)
    return HttpResponse(template.render(context, request))


@login_required
def execute_query(request):
    raw_query = request.GET.get('query')
    db_name = request.user.username
    try:
        query = Query(db_name, raw_query)
    except QueryExecutionError as e:
        return HttpResponseBadRequest(content=str(e))
    context = {
        'query_title': raw_query,
        'column_names': query.get_column_names(),
        'is_dml': query.is_dml,
        'records': query.get_query_result(),
    }
    template = loader.get_template('app/query.html')
    return HttpResponse(template.render(context, request))


def _get_table_context(table, db):
    return {
        'column_names': table.get_columns(),
        'records': table.get_all_records(),
        'table_names': db.get_public_tables(),
        'current_table_name': table.table_name,
        'table_title': 'All',
    }
