$("#table_rows_area").pagination({
    pages: $("#paginate_table_rows").attr("pages"),
    itemOnPage: $("#paginate_table_rows").attr("items_on_page"),
    currentPage: $("#paginate_table_rows").attr("current_page"),
    cssStyle: "page-item",
    prevText: "<span aria-hidden="true" class="page-item">&laquo;</span>",
    nextText: "<span aria-hidden="true">&raquo;</span>",
    onInit() {
        // fire first page loading
    },
    onPageClick: function (page, evt) {
        window.location.href = $("#paginate_table_rows").attr("table_url") + "?page=" + page;
    }
});