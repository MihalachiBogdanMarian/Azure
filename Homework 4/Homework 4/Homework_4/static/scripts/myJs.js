$('#myModal').on('shown.bs.modal', function () {
    $('#myInput').trigger('focus');
})

$(function () {
    $('#btnSearch').click(function (e) {
        e.preventDefault();
        $.ajax({
            url: '/searchPhoto',
            data: $('form').serialize(),
            type: 'POST',
            success: function (response) {
                $("#imagesRes").html("<div class='imagesList'></div>");
                var urlArray = response.split(", ");
                $.each(urlArray, function (l) {
                    if (l === 0) {
                        $(".imagesList").append("<div><img onclick=\"imageProcessing(this)\" data-toggle=\"modal\" data-target=\"#exampleModal\" width=\"300\" height=\"300\" src=" + urlArray[l].split("[")[1] + "/></div>");
                    }
                    else if (l === urlArray.length - 1) {
                        $(".imagesList").append("<div><img onclick=\"imageProcessing(this)\" data-toggle=\"modal\" data-target=\"#exampleModal\" width=\"300\" height=\"300\"src=" + urlArray[l].split("]")[0] + "/></div>");
                    }
                    else {
                        $(".imagesList").append("<div><img onclick=\"imageProcessing(this)\" data-toggle=\"modal\" data-target=\"#exampleModal\" width=\"300\" height=\"300\"src=" + urlArray[l] + "/></div>");
                    }
			    });
            },
            error: function (error) {
                console.log(error);
            }
        });
    });

});

function imageProcessing(image) {
    var url_img = "/getProp/" + image.getAttribute("src").split("https://")[1];
    $.ajax({
        url: url_img,
        data: $('form').serialize(),
        type: 'POST',
        success: function (response) {
            var p = document.getElementById("azureSentence");
            p.innerHTML = response;
        },
        error: function (error) {
            console.log(error);
        }
    });

    $('#addInBd').click(function (e) {
        var url = image.getAttribute("src").split("https://")[1];
        var description = document.getElementById("azureSentence").innerHTML;
        var urlBd = "/addInBd/" + url + "/" + description;
        $.ajax({
            url: urlBd,
            data: $('form').serialize(),
            type: 'POST',
            success: function (response) {
                console.log(response);
            },
            error: function (error) {
                console.log(error);
            }
        });
    });
}

function deleteSentence() {
    var p = document.getElementById("azureSentence");
    p.innerHTML = "";
}