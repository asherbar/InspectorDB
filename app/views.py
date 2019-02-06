import math

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
    template = loader.get_template('app/table_index.html')
    try:
        public_tables = db.get_public_tables()
    except DbConnectionError as e:
        context = {
            'connection_error': True,
            'connection_error_msg': str(e),
            'db_name': db_name

        }
        return HttpResponse(template.render(context, request))
    default_table_name = next(public_tables, None)
    if default_table_name is not None:
        return redirect(get_table.view_name, table_name=default_table_name)
    else:
        context = {
            'no_tables': True,
            'db_name': db_name
        }
        return HttpResponse(template.render(context, request))


table_index.view_name = 'table_index'


@login_required
def get_table(request, table_name):
    db_name = request.user.username
    template = loader.get_template('app/table.html')
    try:
        table = Table(db_name, table_name)
    except TableDoesNotExist:
        raise Http404(f"Table {table_name} does't exist")
    except DbConnectionError:
        return redirect(table_index.view_name)
    db = Db(db_name)
    page = int(request.GET.get('page', 1))
    current_records_page = table.get_records_by_page(page)
    context = {
        'column_names': table.get_columns(),
        'records': current_records_page,
        'table_names': db.get_public_tables(),
        'current_table_name': table.table_name,
        'total_number_of_rows': table.get_total_number_of_rows(),
        'items_on_page': table.limit,
        'current_page': page,
        'number_of_pages': math.ceil(table.get_total_number_of_rows() / table.limit)
    }
    return HttpResponse(template.render(context, request))


get_table.view_name = 'table'


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


execute_query.view_name = 'query'
