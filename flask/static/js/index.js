
function load_body()
{

    $( "#area" ).load( "/userinfo", function() {
        
    });

}



function get_body(path)
{


    $( "#area" ).load( path, function() {
        
    });

}

function close_modal()
{
    var modal = document.getElementById("myModal");
    modal.style.display = "none";
}


function send_git()
{

    var name = $('#name').val();
    var url = $('#url').val();

    if(name.length == 0)
    {
        alert('Name is empty.');
        return;
    }

    if(url.length == 0)
    {
        alert('Url is empty.');
        return;
    }

    if(url.startsWith('http') == false)
    {
        alert('Url starts with http');
        return;
    }

    var jsonData = {
        "name" : name,
        "url" : url
    };

    var reqURL = "/git";

    $.ajax({
        url: reqURL,
        data: JSON.stringify(jsonData),
        type: "POST",
        async: true,
        dataType: "JSON",
        contentType: "application/json; charset=utf-8",
                        
        success: function(response) {
            console.log("");
            console.log("[requestPostBodyJson] : [response] : " + JSON.stringify(response));    				
            console.log("");
            close_modal();

            getvalues();


        },
                        
        error: function(xhr) {
            console.log("");
            console.log("[requestPostBodyJson] : [error] : " + JSON.stringify(xhr));
            console.log("");    				
        },
                        
        complete:function(data,textStatus) {
            console.log("");
            console.log("[requestPostBodyJson] : [complete] : " + textStatus);
            console.log("");    				
        }
    });	

}

