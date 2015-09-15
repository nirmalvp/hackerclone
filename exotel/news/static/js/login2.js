$('#comment-button').click(function() {
23     $('#form-modal-body').load('/test-form/', function () {
24         $('#form-modal').modal('toggle');
25         formAjaxSubmit('#form-modal-body form', '#form-modal');
26});
