
var formAjaxSubmit = function(form, modal) {
   $(form).submit(function (e) {
      console.log($(this).attr('method'))
      console.log($(this).attr('action'))
      console.log($(this).serialize())

      e.preventDefault();
      $.ajax({
          type: $(this).attr('method'),
          url: $(this).attr('action'),
          data: $(this).serialize(),
          success: function (xhr, ajaxOptions, thrownError) {
             console.log(xhr)
              if ( $(xhr).find('.errorlist').length > 0 ) {
               $(modal).find('.modal-body').html(xhr);
               formAjaxSubmit(form, modal);
           } else {
               $(modal).modal('toggle');
           }
       },
       error: function (xhr, ajaxOptions, thrownError) {
        console.log("error")
                 // handle response errors here
             }
         });
  });
}
$("#myModal").on("show.bs.modal", function(e) {
    var link = $(e.relatedTarget);
    $(this).find(".modal-body").load(link.attr("href"),function () {
      formAjaxSubmit('#form-modal-body form', '#myModal')
    });
});

$('#myModal').on('hidden.bs.modal', function () {
    window.location.reload(true);
});
