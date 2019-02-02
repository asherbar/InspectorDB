from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404
from django.shortcuts import redirect
from django.template import loader

from app.logic.db.db import Db
from app.logic.db.query import Query, QueryExecutionError
from app.logic.db.table import Table, TableDoesNotExist
from app.logic.utils.db_connection import DbConnectionError
from app.logic.utils.logger_utils import get_logger

logger = get_logger(__name__)


@login_required
def table_index(request):
    db_name = request.user.username

    db = Db(db_name)
    try:
        public_tables = db.get_public_tables()
    except DbConnectionError:
        return HttpResponse('No connection')
    default_table_name = next(public_tables, None)
    if default_table_name is not None:
        return redirect('table', table_name=default_table_name)
    else:
        template = loader.get_template('app/table_index.html')
        return HttpResponse(template.render(request=request))


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
    template = loader.get_template('app/query.html')
    try:
        query = Query(db_name, raw_query)
    except QueryExecutionError as e:
        context = {
            'query_error': True,
            'error_msg': str(e)
        }
        return HttpResponse(template.render(context, request))
    context = {
        'query_error': False,
        'query_title': raw_query,
        'column_names': query.get_column_names(),
        'is_dml': query.is_dml,
        'records': query.get_query_result(),
    }
    return HttpResponse(template.render(context, request))


def _get_table_context(table, db):
    return {
        'column_names': table.get_columns(),
        'records': table.get_all_records(),
        'table_names': db.get_public_tables(),
        'current_table_name': table.table_name,
        'table_title': 'All',
    }
