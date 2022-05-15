
$(document).ready(function () {
    $(".form-group > div > input").css("margin-bottom", "15px");
});

function openAddNewDeviceModal(organizationId) {
    loginCheck();
    fillCatalogDropdown();
    $("#addNewDeviceToOrganizationId").val(organizationId);
    $("#addDeviceModal").modal("show");
}

//111
function openAddNewPartModal(deviceId) {
    loginCheck();
    $("#addPartModalDeviceId").val(deviceId);
    $("#addPartModal").modal("show");
}

function openNotificationTimeLimitModal() {
    loginCheck("setNotificationTimeLimitModal");
    //$("#setNotificationTimeLimitModal").modal("show");
}

function openAddNewOrganizationModal() {
    loginCheck("addOrganizationModal");
    //$("#addOrganizationModal").modal("show");
}

function openAddNewDeviceToCatalog() {
    loginCheck("addDeviceToCatalogModal");
}

function loginCheck(openModalElementId = null) {
    $.ajax({
        type: 'GET',
        url: '/loginCheck',
        data: {},
        dataType: 'json',
        success: function (data) {
            if (data.isLogin == "False") { window.location.href = "/accounts/login/"; }
            else if (openModalElementId != null) { $("#" + openModalElementId).modal("show"); }
        }
    });
}

function fillCatalogDropdown() {
    $.ajax({
        type: 'GET',
        url: '/catalog',
        data: {},
        dataType: 'json',
        success: function (data) {
            var options = '';

            $.each(data.devices, function (index, device) {
                options += '<option value="' + device.Id + '">Product No :  ' + device.ProductNo + ' </option>';
            });

            $("#id_addDevice_catalogDeviceId").html(options)
        }
    });
}

function addDevice() {

    $.ajax({
        type: 'get',
        url: '/addDevice',
        data: {
            description: $("#id_addDevice_description").val(),
            organizationId: $("#addNewDeviceToOrganizationId").val(),
            catalogDeviceId: $("#id_addDevice_catalogDeviceId").val()
        },
        datatype: 'json',
        success: function (data) {
            $('body').removeClass('modal-open');
            $('.modal-backdrop').remove();
            $('#addDeviceModal').modal("hide");
            showMessage('Adding new device is successful.');
            getDevices($("#addNewDeviceToOrganizationId").val());
        }
    });
}

function addDeviceToCatalog() {

    if ($("#id_addCatalog_productNo").val() == "") { showMessage("Product no is required.", false); }
    else if ($("#id_addCatalog_type").val() == "") { showMessage("Type is required.", false); }
    else if ($("#id_addCatalog_description").val() == "") { showMessage("Description is required.", false); }
    else {
        $.ajax({
            type: 'GET',
            url: '/addDeviceToCatalog',
            data: {
                type: $("#id_addCatalog_type").val(),
                productNo: $("#id_addCatalog_productNo").val(),
                description: $("#id_addCatalog_description").val(),
            },
            dataType: 'json',
            success: function (data) {
                $('body').removeClass('modal-open');
                $('.modal-backdrop').remove();
                $('#addDeviceToCatalogModal').modal("hide");
                showMessage('Adding new device is successful to catalog.');
                getCatalog();
            }
        });
    }


}



function setNotificationTimeLimit() {
    if ($('#id_notificationTimeLimit').val() == "") {
        showMessage("Notification time limit is required.", false);
    } else {
        $.ajax({
            type: 'GET',
            url: '/setNotificationTime',
            data: { notificationTimeLimit: $("#id_notificationTimeLimit").val() },
            dataType: 'json',
            success: function (data) {
                $('body').removeClass('modal-open');
                $('.modal-backdrop').remove();
                $('#setNotificationTimeLimitModal').modal("hide");
                showMessage('Notification time limit editing is OK.');
                getOrganizations();
            }
        });
    }


}

function addOrganization() {

    if ($("#id_organizationName").val() == "") { showMessage("Organization name is required.", false); }
    else {
        $.ajax({
            type: 'GET',
            url: '/addOrganization',
            data: { organizationName: $("#id_organizationName").val() },
            dataType: 'json',
            success: function (data) {
                $('body').removeClass('modal-open');
                $('.modal-backdrop').remove();
                $('#addOrganizationModal').modal("hide");
                showMessage('Adding new organization successful.');
                getOrganizations();
            }
        });

    }



}
function addPart() {
    if ($("#id_productNo").val() == "") { showMessage("Product No is required.", false); }
    else if ($("#id_type").val() == "") { showMessage("Type is required.", false); }
    else if ($("#addPartModal #id_description").val() == "") { showMessage("Description is required.", false); }
    else if ($("#id_totalLifeTime").val() == "") { showMessage("Total Life Time is required.", false); }
    else if ($("#id_price").val() == "") { showMessage("Price is required.", false); }
    else {

        $.ajax({
            type: 'GET',
            url: '/addPart',
            data: {
                deviceId: $("#addPartModalDeviceId").val(),
                productNo: $("#id_productNo").val(),
                type: $("#id_type").val(),
                description: $("#addPartModal #id_description").val(),
                totalLifeTime: $("#id_totalLifeTime").val(),
                price: $("#id_price").val()
            },
            dataType: 'json',
            success: function (data) {
                $('body').removeClass('modal-open');
                $('.modal-backdrop').remove();
                $('#addPartModal').modal("hide");
                showMessage('Adding new part is successful.');
                getParts($("#addPartModalDeviceId").val());
            }
        });

    }

}
function attach(organizationId) {

    $.ajax({
        type: 'GET',
        url: '/attach',
        data: { organizationId: organizationId },
        dataType: 'json',
        success: function (data) {
            showMessage('Organization is attached.');
            getOrganizations();
        }
    });
}
function detach(organizationId) {

    $.ajax({
        type: 'GET',
        url: '/detach',
        data: { organizationId: organizationId },
        dataType: 'json',
        success: function (data) {
            showMessage('Organization is detached.');
            getOrganizations();
        }
    });
}

function shareUnShareOrganization(organizationId, type) {

    $.ajax({
        type: 'GET',
        url: '/shareUnShareOrganization',
        data: { type: type, organizationId: organizationId },
        dataType: 'json',
        success: function (data) {
            var htmlData = '<h1>Share/Unshare Organization</h1><div><table class="table table-bordered table-hover"><thead><tr><th>#</th><th>Id</th><th>Username</th><th>Choice</th></tr></thead><tbody>';

            $.each(data.users, function (index, user) {
                htmlData += '<tr><td>' + index + '  </td><td>' + user.Id + '  </td><td>' + user.Username + '  </td>';
                if (type == "1")//share
                    htmlData += '<td><a href="#" onclick="shareUnshareSubmit(' + '\'' + organizationId + '\'' + ',' + user.Id + ',1) ">Share</td></tr>';
                else htmlData += '<td><a href="#" onclick="shareUnshareSubmit(' + '\'' + organizationId + '\'' + ',' + user.Id + ',2) ">UnShare</td></tr>';
            }
            );

            htmlData += "</tbody></table></div>";

            $(".body-content").html(htmlData)

        }
    });
}

function shareUnshareSubmit(organizationId, userId, type) {

    $.ajax({
        type: 'GET',
        url: '/shareUnShareOrganization',
        data: { organizationId: organizationId, selectedUserId: userId, type: type, submit: "True" },
        dataType: 'json',
        success: function (data) {
            if (data.result == "OK") { showMessage(type == "1" ? "Sharing is OK." : "Unsharing is OK."); shareUnShareOrganization(organizationId, type); }
        }
    });

}

function getCatalog() {

    $("#id_getParts_deviceId").val("");

    $.ajax({
        type: 'GET',
        url: '/catalog',
        data: {},
        dataType: 'json',
        success: function (data) {
            var htmlData = '<h1>Device List</h1><div><table class="table table-bordered table-hover"><thead><tr><td>#</td><th>Id</th><th>Product No</th><th>Type</th><th>Description</th><th>Is On</th></tr></thead><tbody>';

            $.each(data.devices, function (index, device) {
                htmlData += '<tr><td>' + index + '</td><td>' + device.Id + '</td><td>' + device.ProductNo + '</td><td>' + device.Type + '</td><td>' + device.Description + '</td><td>' + device.IsOn + '</td><td><a href="#" onclick="getParts(' + '\'' + device.Id + '\'' + ')">Part(s)</a></td> <td><a href="#" onclick="openAddNewPartModal(' + '\'' + device.Id + '\'' + ')">Add Part</a></td> </tr>';
            }
            );

            htmlData += "</tbody></table></div>";

            $(".body-content").html(htmlData)
        }
    });
}
function getDevices(organization_id) {

    $.ajax({
        type: 'GET',
        url: '/devices',
        data: { organizationId: organization_id },
        dataType: 'json',
        success: function (data) {
            var htmlData = '<h1>Device List</h1><div><table class="table table-bordered table-hover"><thead><tr><td>#</td><th>Id</th><th>Product No</th><th>Type</th><th>Description</th><th>Is On</th></tr></thead><tbody>';

            $.each(data.devices, function (index, device) {
                htmlData += '<tr><td>' + index + '</td><td>' + device.Id + '</td><td>' + device.ProductNo + '</td><td>' + device.Type + '</td><td>' + device.Description + '</td><td>' + device.IsOn + '</td><td><a href="#" onclick="getParts(' + '\'' + device.Id + '\'' + ')">Part(s)</a></td><td><a href="#" onclick="openAddNewPartModal(' + '\'' + device.Id + '\'' + ')">Add Part</a></td> ';

                if (device.IsOn == "On") htmlData += '<td><a href="#" onclick="onOff(' + '\'' + organization_id + '\'' + ',' + '\'' + device.Id + '\'' + ',0)">Off</a></td>';
                else htmlData += '<td><a href="#" onclick="onOff(' + '\'' + organization_id + '\'' + ',' + '\'' + device.Id + '\'' + ',1)">On</a></td>';

                htmlData += "</tr>";
            }
            );

            htmlData += "</tbody></table></div>";

            $(".body-content").html(htmlData)
        }
    });
}
function getParts(device_id) {

    $("#id_getParts_deviceId").val(device_id);

    $.ajax({
        type: 'GET',
        url: '/parts',
        data: { deviceId: device_id },
        dataType: 'json',
        success: function (data) {
            var htmlData = '<h1>Part List</h1><div><table class="table table-bordered table-hover"><thead><tr><th>Device No</th><th>Part No</th><th>Description</th><th>Type</th><th>T.L.Time</th><th>R.L.Time</th><th>Price</th></tr></thead><tbody>';

            $.each(data.parts, function (index, part) {
                htmlData += '<tr><td>' + part.Device_ProductNo + '</td><td>' + part.Part_ProductNo + '</td><td>' + part.Description + '</td><td>' + part.Type + '</td><td>' + part.TotalLifeTime + '</td><td>' + part.ExpectedLifeTime + '</td><td>' + part.Price + '</td><td><a href="#" onclick="removePart(' + '\'' + part.DeviceId + '\'' + ',' + '\'' + part.Id + '\'' + ' )">Remove</a></td></tr>';
            }
            );

            htmlData += "</tbody></table></div>";

            $(".body-content").html(htmlData)
        }
    });
}

function removePart(deviceId, partId) {

    $.ajax({
        type: 'GET',
        url: '/removePart',
        data: { partId: partId },
        dataType: 'json',
        success: function (data) {
            if (data.result == "OK") { showMessage("Removing part is OK."); getParts(deviceId); }
        }
    });
}
function onOff(organizationId, deviceId, setOn) {

    var url = setOn == "1" ? "on" : "off"
    $.ajax({
        type: 'GET',
        url: "/" + url,
        data: { deviceId: deviceId },
        dataType: 'json',
        success: function (data) {
            if (data.result == "OK") { showMessage("Device is " + url.toUpperCase()); getDevices(organizationId); }
            else { showMessage(data.result, false); }
        },
        error: function (request, status, error) {
            alert(request.responseText);
        }
    });
}

function getOrganizations() {

    $("#id_getParts_deviceId").val("");

    $.ajax({
        type: 'GET',
        url: '/organizations',
        data: {},
        dataType: 'json',
        success: function (data) {
            var htmlData = '<h1>Organization List</h1><div><table class="table table-bordered table-hover"><thead><tr><th>#</th><th>Id</th><th>Name</th><th>Is Attached</th></tr></thead><tbody>';

            $.each(data.organizations, function (index, organization) {
                htmlData += '<tr><td>' + index + '</td><td>' + organization.Id + '</td><td>' + organization.Name + '</td><td>' + organization.IsAttached + '</td>';
                if (organization.IsAttached == "True") {
                    htmlData += '<td><a href="#" onclick="detach(' + '\'' + organization.Id + '\'' + ')">Detach</a></td>';
                } else {
                    htmlData += '<td><a href="#" onclick="attach(' + '\'' + organization.Id + '\'' + ')">Attach</a></td>';
                }

                htmlData += '<td><a href="#" onclick="shareUnShareOrganization(' + '\'' + organization.Id + '\'' + ',1)">Share</a></td>';
                htmlData += '<td><a href="#" onclick="shareUnShareOrganization(' + '\'' + organization.Id + '\'' + ',2)">UnShare</a></td>';
                htmlData += '<td><a href="#" onclick="getDevices(' + '\'' + organization.Id + '\'' + ')">Devices</a></td>';
                htmlData += '<td><a href="#" onclick="openAddNewDeviceModal(' + '\'' + organization.Id + '\'' + ')">Add Device</a></td>';
            }
            );

            htmlData += "</tbody></table></div>";

            $(".body-content").html(htmlData)
        }
    });
}

function showMessage(message, isSuccess = true) {
    if (isSuccess == false) { $("#messageText").text('❌' + message); }
    else $("#messageText").text('✔️ ' + message);


    $("#messageModal").modal("show");
}