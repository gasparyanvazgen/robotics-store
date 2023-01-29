$(document).ready(function() {
    $('#categorySelect .option').on('change', function() {
        document.getElementById("filter-form").submit();
    });
    $('#availabilitySelect').on('change', function() {
        document.getElementById("filter-form").submit();
    });
    $('#searchInput').on('keyup', function(event) {
        if (event.keyCode === 13) {
            document.getElementById("filter-form").submit();
        }
    });
    $('#search').on('click', function() {
        document.getElementById("filter-form").submit();
    });
});
