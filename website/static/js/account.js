$(document).ready(function () {
    function load_data(value = 0, page = 1) {
        $.ajax({
            type: "POST",
            url: "http://127.0.0.1:5000/signatureCategory",
            data: { 
                value: value, // Displays your verified list of signature which you use your own signature as comparison
                page: page
            },
            dataType: "JSON",
            success: function (response) {
                let data = response.listSignatures
                let totalPages = response.totalPages
                let start = response.start
                $("#signatureTable tbody").empty();

                for (var i = 0; i < data.length; i++) {
                    let row = '<tr>';
                    row += '<th scope="row">' + (start + i + 1) + '</th>';
                    row += '<td>' + data[i][0] + '</td>';
                    row += '<td>' + data[i][1] + '</td>';
                    row += '<td>' + data[i][2] + '</td>';  
                    row += '<td>' + data[i][3] + '</td>'; 
                    row += '<td>' + data[i][4] + '</td>'; 
                    row += '</tr>';
                    $("#signatureTable tbody").append(row);
                }

                $("#pagination").empty();

                if (page == 1) {
                    paginationPage = '<li class="page-item" page="'+ page +'"><a class="page-link" href="#signatureTable">Previous</a></li>'
                }
                else {
                    paginationPage = '<li class="page-item" page="' + (page - 1) +'"><a class="page-link" href="#signatureTable">Previous</a></li>'
                }
                $("#pagination").append(paginationPage);

                for (var i = 0; i < totalPages; i++) {
                    paginationPage = '<li class="page-item" page="'+ (i + 1) + '">';
                    paginationPage += '<a class="page-link" href="#signatureTable">' + (i + 1) + "</a>";
                    paginationPage += "</li>"
                    $("#pagination").append(paginationPage); 
                }

                if (page == totalPages) {
                    paginationPage = '<li class="page-item disable" page="' + page +'"><a class="page-link" href="#signatureTable">Next</a></li>'
                }
                else {
                    paginationPage = '<li class="page-item disable" page="' + (page + 1) +'"><a class="page-link" href="#signatureTable">Next</a></li>'
                }
                $("#pagination").append(paginationPage);
                
            },
            error: function (response) {
                console.log(response);
            }
        });
    }
    load_data();
    
    
    $("#signatureCategory").change(function () {
        let value = $(this).val()

        load_data(value);
    })

    $("#pagination").on('click', '.page-item', function () {
        let page = parseInt($(this).attr('page'));
        let value = $("#signatureCategory").val()

        load_data(value, page)
    });
    
    $("#userUploadSignature").change(function () { 
        const file = this.files[0];
        if (file) {
            let reader = new FileReader();
            reader.onload = function(event){
                $('#userSignature').attr('src', event.target.result);
            }
            reader.readAsDataURL(file);
        }
    });

    $("#verifySignatureInput").change(function () { 
        const file = this.files[0];
        if (file) {
            let reader = new FileReader();
            reader.onload = function(event){
                $('#verifySignatureImage').attr('src', event.target.result);
            }
            reader.readAsDataURL(file);
        }
    });

    $("#verifySignature").click(function (e) { 
        let verifySignatureInput = $("#verifySignatureInput")[0];
        let verifySignature = verifySignatureInput.files[0];

        let formData = new FormData();
        formData.append('verifySignature', verifySignature)

        $.ajax({
            type: "POST",
            url: "http://127.0.0.1:5000/verifySignature",
            data: formData,
            processData: false,
            contentType: false,
            success: function(response) {
                let parameters = $.param(response);
                window.location.href = "http://127.0.0.1:5000/result" + "?" + parameters;
            },
            error: function (response) {
                console.log(response);
            }
        });
        
    });

    $("#saveUserSignature").click(function() {
        let userSignatureInput = $("#userUploadSignature")[0];
        let userSignature = userSignatureInput.files[0];

        let formData = new FormData();
        formData.append('userSignature', userSignature)

        $.ajax({
            type: "POST",
            url: "http://127.0.0.1:5000/changeSignature",
            data: formData,
            processData: false,
            contentType: false,
            success: function (response) {
                $('#currentUserSignature').attr('src', "../static/sign_storage/" + response.userSignature_sec);
            },
            error: function (response) {
                console.log(response);
            }
        });
        $("#signatureModal").modal('hide')
    })
});