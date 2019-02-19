from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import redirect, render

from app.logic.db.db import Db
from app.logic.db.table import Table, TableDoesNotExist
from app.logic.utils.db_connection import DbConnectionError


class TableView:
    view_name = 'table'
    template_path = 'app/table.html'

    def __init__(self, db_name, table_name, page):
        self.db_name = db_name
        self.table_name = table_name
        self.page = page

    def dispatch(self, request):
        try:
            table = Table(self.db_name, self.table_name)
        except TableDoesNotExist:
            raise Http404(f"Table {self.table_name} does't exist")
        except DbConnectionError:
            # Imported locally to avoid circular dependency
            from app.views.index_view import IndexView
            return redirect(IndexView.view_name)
        db = Db(self.db_name)
        page = self.page or 1
        try:
            page = int(page)
        except ValueError:
            page = -1
        if page <= 0:
            return redirect(self.view_name, table_name=self.table_name)
        current_records_page = table.get_records_by_page(page)
        context = {
            'column_names': table.get_columns(),
            'records': current_records_page,
            'table_names': db.get_public_tables(),
            'current_table_name': table.table_name,
            'total_number_of_rows': table.get_total_number_of_rows(),
            'items_on_page': table.limit,
            'current_page': page,
            'number_of_pages': int(1 + (table.get_total_number_of_rows() / table.limit))
        }
        return render(request, self.template_path, context)

    @classmethod
    def as_view(cls):
        @login_required
        def view(request, table_name):
            table_view = TableView(request.user.username, table_name, request.GET.get('page'))
            return table_view.dispatch(request)

        return view
