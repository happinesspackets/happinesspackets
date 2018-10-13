$(document).ready(function($){

    $(document).on('click', '#archive_load_more', function() {

        // on clicking "Load more" button, fetch the data from given url and display it in the current list 
        $('#archive_more_content').load("/archive/load-more/", function(response, status, xhr){
            if (status == "error")
                alert(xhr.status + " " + xhr.statustext);
            else
                $('#archive_load_more').hide();
        })
    })
})