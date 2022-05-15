
var userId = null;

function _loginCheck() {
    $.ajax({
        type: 'GET',
        url: '/loginCheck',
        data: {},
        dataType: 'json',
        success: function (data) {
           
            if (data.isLogin == "False") {
                if (window.location.href.endsWith("/accounts/login/") == false)
                    window.location.href = "/accounts/login/";
            }
            else { userId = data.userId; console.log(data); }
        }
    });
}

_loginCheck();

var alreadyNotifications = []
let url = `ws://${window.location.host}/ws/socket-server/`
console.log(url)

const chatSocket = new WebSocket(url)

chatSocket.onmessage = function (e) {
    let data = JSON.parse(e.data)
    
    if (data.type === 'chat' && userId != null) {
        let messages = document.getElementById('messages')

        $.each(data.message.notifications, function (index, notification) {

            if (notification.UserId == userId && alreadyNotifications.includes(JSON.stringify(notification)) == false) {
                setTimeout(function () {
                    toastr.options = {
                        closeButton: true,
                        progressBar: true,
                        //showMethod: 'slideDown',
                        "showMethod": "fadeIn",
                        "hideMethod": "fadeOut",
                        timeOut: 0,
                        extendedTimeOut: 0,
                        tapToDismiss: false
                    };

                    toastr.warning('<p style="margin-bottom:2px;margin-top:2px;">Device Product No :' + notification.DeviceProductNo + ' </p>' +
                        '<p style="margin-bottom:2px;margin-top:2px;">Part Product No :' + notification.PartProductNo + ' </p>' +
                        '<p style="margin-bottom:2px;margin-top:2px;">Expected Life Time :' + notification.ExpectedLifeTime + ' </p>',
                        '<p style="margin-bottom:2px;margin-top:2px;">Organization Name :' + notification.OrganizationName + ' </p>');

                }, 1300);

                alreadyNotifications.push(JSON.stringify(notification))
            }
        });

        if ($("#id_getParts_deviceId").val() != "") {

            var htmlData = '<h1>Part List</h1><div><table class="table table-bordered table-hover"><thead><tr><th>Device No</th><th>Part No</th><th>Description</th><th>Type</th><th>T.L.Time</th><th>R.L.Time</th><th>Price</th></tr></thead><tbody>';
            
            $.each(data.message.partsData, function (index, part) {
                
                if (part.DeviceId == $("#id_getParts_deviceId").val()) {
                    htmlData += '<tr><td>' + part.Device_ProductNo + '</td><td>' + part.Part_ProductNo + '</td><td>' + part.Description + '</td><td>' + part.Type + '</td><td>' + part.TotalLifeTime + '</td><td>' + part.ExpectedLifeTime + '</td><td>' + part.Price + '</td><td><a href="#" onclick="removePart(' + '\'' + part.DeviceId + '\'' + ',' + '\'' + part.Id + '\'' + ' )">Remove</a></td></tr>';
                }
            });

            htmlData += "</tbody></table></div>";

            $(".body-content").html(htmlData)
        }
    }
}

let form = document.getElementById('form')
form.addEventListener('submit', (e) => {
    e.preventDefault()
    let message = e.target.message.value
    chatSocket.send(JSON.stringify({
        'message': message
    }))
    form.reset()
})
