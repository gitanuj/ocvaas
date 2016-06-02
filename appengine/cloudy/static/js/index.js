$(document).ready(function() {

    function updateDialog(job, status, result) {
        $('#myModal').modal('show');
        $('#status_table').empty();

        if (status == "Successful") {
            $('#status_table').append('<tr><td>' + job + '</td>' + '<td>' + status + '</td>' + '<td>' + '<a target="_blank" href= ' + result + '>View image</a>' + '</td>' + '</tr>');
        } else {
            $('#status_table').append('<tr><td>' + job + '</td>' + '<td>' + status + '</td>' + '<td>' + '</td>' + '</tr>');
        }
    }

    function fetchStatus(id) {

        var job = id;
        console.log(job);

        $.ajax({

            url: "/api/" + job,
            type: "GET",
            dataType: "json",
            success: function(data) {

                var items = [];
                var status_code = data.status;
                var status;
                switch (status_code) {
                    case 4:
                        status = "Successful";
                        break;
                    case 3:
                        status = "Failed";
                        break;
                    case 2:
                        status = "Started";
                        break;
                    case 1:
                        status = "Submitted";
                        break;
                }

                var result = data.res;
                console.log(status);
                console.log(result);
                updateDialog(job, status, result)
                if (status == "Submitted" || status == "Started") {
                    fetchStatus(job);
                }
            }
        });
    }

    $("#get_button").click(function() {

        $('#myModal').modal('show');
        var job = $('#job_id')[0].value;
        console.log(job);
        fetchStatus(job);
    });


    $("#submit_button").click(function() {

        console.log('submit clicked');
        var filters = $('#filters')[0].value;
        var filters_json = JSON.parse(filters);

        updateDialog("Waiting", "...", "");

        $.ajax({

            url: "/api",
            type: "POST",
            data: JSON.stringify(filters_json),
            dataType: "json",
            success: function(data) {
                var id = data.id;
                console.log(id);
                fetchStatus(id);
            }
        });
    });
});