$(document).ready(function() {
    $('#execute_query').click(function() {
        payload = { query: $('#query_input').val(), table: $('#current_table_name').text(), page: $('#paginate_table_rows').attr('current_page') }
        $.get( $('#update_query_results_area').attr('query_url'), payload, function(data) {
            if (!data['query_error'] && data['query_result']) {
                    $('#data_area').empty().append(data['query_result']);
            }
            $('#query_title').empty().append(data['query_title']);
        });
    });
});