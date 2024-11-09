$(function() {
    $("#gene_name").autocomplete({
        source: function(request, response) {
            $.ajax({
                url: "/autocomplete",
                dataType: "json",
                data: {
                    term: request.term
                },
                success: function(data) {
                    response(data);
                }
            });
        },
        minLength: 2,
        select: function(event, ui) {
            $("#gene_name").val(ui.item.value);
            $("#search-form").submit();
        }
    });
});
