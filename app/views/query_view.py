from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import redirect
from django.template.loader import render_to_string

from app.logic.db.query import Query, QueryExecutionError
from app.logic.db.table import Table, TableDoesNotExist
from app.logic.utils.db_connection import DbConnectionError
from app.logic.utils.logger_utils import get_logger
from app.views.index_view import IndexView

logger = get_logger(__name__)


class QueryView:
    view_name = 'query'
    template_path = 'app/query.html'

    def __init__(self, db_name, query, table_name, page):
        self.db_name = db_name
        self.query = query
        self.table_name = table_name
        if page is not None:
            try:
                page = int(page)
            except ValueError:
                page = None
        self.page = page

    def dispatch(self):
        try:
            query = Query(self.db_name, self.query)
        except QueryExecutionError as e:
            return self.create_error_response(e)
        response = {
            'query_error': False,
            'query_title': self.query,
            'query_result': '',
        }
        if query.is_dml:
            if not all((self.table_name, self.page)):
                logger.error(f"table_name and page must not be None. Instead they're: {self.table_name}, {self.page}")
            else:

                try:
                    table = Table(self.db_name, self.table_name)
                except TableDoesNotExist:
                    logger.error(f'No table {self.table_name} exists in database {self.db_name}')
                except DbConnectionError:
                    return redirect(IndexView.view_name)
                else:
                    current_records_page = table.get_records_by_page(self.page)
                    context = {
                        'column_names': table.get_columns(),
                        'records': current_records_page,
                    }
                    response['query_result'] = render_to_string(self.template_path, context)
        else:
            context = {
                'column_names': query.get_column_names(),
                'records': query.get_query_result(),
            }
            response['query_result'] = render_to_string(self.template_path, context)
        return JsonResponse(response)

    @staticmethod
    def create_error_response(e):
        response = {
            'query_error': True,
            'query_title': str(e)
        }
        return JsonResponse(response)

    @classmethod
    def as_view(cls, ):
        @login_required
        def view(request):
            query_view = QueryView(request.user.username, request.GET.get('query'), request.GET.get('table'),
                                   request.GET.get('page'))
            return query_view.dispatch()

        return view
