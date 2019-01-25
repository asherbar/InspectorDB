$(document).ready(function() {
    $('#execute_query').click(function() {
        $.get( $('#update_query_results_area').attr('query_url'), { query: $('#query_input').val() }, function(data) {
            $('#query_results_area').empty().append(data).removeAttr('hidden');
        });
    });
});