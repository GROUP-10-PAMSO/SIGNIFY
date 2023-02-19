$(document).ready(function () {
    $.ajax({
        type: "POST",
        url: "http://127.0.0.1:5000/signatureCategory",
        data: { 
            value: 0 // Displays your verified list of signature which you use your own signature as comparison 
        },
        dataType: "JSON",
        success: function (response) {
            let data = response.result
            for (var i = 0; i < data.length; i++) {
                let row = '<tr>';
                row += '<th scope="row">' + i + '</th>';
                row += '<td>' + data[i][0] + '</td>';
                row += '<td>' + data[i][1] + '</td>';
                row += '<td>' + data[i][2] + '</td>';  
                row += '<td>' + data[i][3] + '</td>'; 
                row += '</tr>';
                $("#signatureTable tbody").append(row);
            }
        },
        error: function (response) {
            console.log(response);
        }
    });
    
    $("#signatureCategory").change(function () {
        let value = $(this).val()

        $.ajax({
            type: "POST",
            url: "http://127.0.0.1:5000/signatureCategory",
            data: { 
                value: value 
            },
            dataType: "JSON",
            success: function (response) {
                let data = response.result
                $("#signatureTable tbody").empty();
                
                for (var i = 0; i < data.length; i++) {
                    let row = '<tr>';
                    row += '<th scope="row">' + i + '</th>';
                    row += '<td>' + data[i][0] + '</td>';
                    row += '<td>' + data[i][1] + '</td>';
                    row += '<td>' + data[i][2] + '</td>';  
                    row += '<td>' + data[i][3] + '</td>'; 
                    row += '</tr>';
                    $("#signatureTable tbody").append(row);
                }
            },
            error: function (response) {
                console.log(response);
            }
        });
    })
    
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