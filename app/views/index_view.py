from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from app.logic.db.db import Db
from app.logic.utils.db_connection import DbConnectionError
from app.views.table_view import TableView


class IndexView:
    view_name = 'table_index'
    template_path = 'app/table_index.html'

    def __init__(self, db_name):
        self.db_name = db_name

    def dispatch(self, request):
        db = Db(self.db_name)
        try:
            public_tables = db.get_public_tables()
        except DbConnectionError as e:
            context = {
                'connection_error': True,
                'connection_error_msg': str(e),
                'db_name': self.db_name

            }
            return render(request, self.template_path, context)
        default_table_name = next(public_tables, None)
        if default_table_name is not None:
            return redirect(TableView.view_name, table_name=default_table_name)
        else:
            return render(request, 'app/no_tables.html')

    @classmethod
    def as_view(cls):
        @login_required
        def view(request):
            index_view = IndexView(request.user.username)
            return index_view.dispatch(request)

        return view
