$('#loading').hide();
$('#linkurl').on('input', function() {
    $('#linktitle').val('');
    $('#submit').attr('disabled', 'disabled');
});

$("#getTitle").click(function(event){
    var linkurl = $('#linkurl').val();
    if (!/^https?:\/\//i.test(linkurl)) {
        linkurl = 'http://' + linkurl;
        $('#linkurl').val(linkurl);
    }
    event.preventDefault();
    $('#loading').show();
    $.ajax({
        url: '/gettitle/',
        type: "POST",
        data: {link:linkurl},
        success: function(json) {
            $('#loading').hide();
            if (json.error){
                $('#linktitle').val("Could not fetch title")
            }
            else{
                $('#linktitle').val(json.pageTitle);
                $('#submit').removeAttr('disabled');

            }

         }
    });

});



