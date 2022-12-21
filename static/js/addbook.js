

function deletealert(val) {
    swal({
        title: "Your Book will be deleted permanently!",
        text: "Are you sure to proceed?",
        type: "warning",
        showCancelButton: true,
        confirmButtonColor: "#DD6B55",
        confirmButtonText: "Remove Book!",
        cancelButtonText: "I am not sure!",
    })
        .then(isConfirm => {
            if (isConfirm.value) {
                $.ajax({
                url: '/delete-book/'+val+'/',
                success: function (data) {
                    swal("Book Removed!", "Your Book is removed permanently!", "success");
                    setTimeout(function() {
                    window.location.href= "/show-book-table/";
                    }, 2000);

                }

                });

            }
            else {
                    swal("Oops", "Book is not removed!", "error");
                    setTimeout(function() {
                    window.location.href= " /show-book-table/";
                    }, 2000);

            }
        })
}