$(function () {

    // ****************************************
    //  U T I L I T Y   F U N C T I O N S
    // ****************************************

    // Updates the form with data from the response
    function update_form_data(res) {
        // console.log("update_form_data: res try")
        // console.log(res)
        addr = res.address;
        $("#customer_id").val(res.customer_id);
        $("#user_id").val(res.user_id);
        $("#first_name").val(res.first_name);
        $("#last_name").val(res.last_name);
        $("#active").val(res.active).change();
        $("#street").val(addr.street);
        $("#apartment").val(addr.apartment);
        $("#city").val(addr.city);
        $("#state").val(addr.state);
        $("#zip_code").val(addr.zip_code);
    }

    // Clears all form fields
    function clear_form_data() {
        $("#customer_id").val();
        $("#user_id").val("");
        $("#first_name").val("");
        $("#last_name").val("");
        $("#password").val("");
        $("#active").val(true).change();

        $("#street").val("");
        $("#apartment").val("");
        $("#city").val("");
        $("#state").val("");
        $("#zip_code").val("");
    }

    // Updates the flash message area
    function flash_message(message) {
        $("#flash_message").empty();
        $("#flash_message").append(message);
    }

    // Puts current customer_id info into bottom search result table
    function show_in_search_results_by_customer_id() {

        var customer_id = $("#customer_id").val();
        var ajax = $.ajax({
            type: "GET",
            url: "/customers/" + customer_id,
            contentType: "application/json",
            data: ''
        })

        ajax.done(function(res){
            $("#search_results").empty();
            $("#search_results").append('<table class="table-striped" cellpadding="10">');
            var header = '<tr>'
            header += '<th style="width:5%">Customer ID</th>'
            header += '<th style="width:10%">User ID</th>'
            header += '<th style="width:15%">First Name</th>'
            header += '<th style="width:15%">Last Name</th>'
            header += '<th style="width:40%">Address</th>'
            header += '<th style="width:15%">Active</th></tr>'
            $("#search_results").append(header);
            var firstCust = "";
            for(var i = 0; i < res.length; i++) {
                var customer = res[i];
                var addr = customer.address
                var row = "<tr><td>"+customer.customer_id+"</td><td>"+customer.user_id+"</td><td>"+customer.first_name+"</td><td>"+customer.last_name+"</td><td>"+
                addr.street+", "+addr.apartment+", "+addr.city+", "+addr.state+" - "+addr.zip_code+"</td><td>"+customer.active+"</td></tr>";
                $("#search_results").append(row);
                if (i == 0) {
                    firstCust = customer;
                }
            }

            $("#search_results").append('</table>');
        });
    }

    // ****************************************
    // Create a Customer
    // ****************************************

    $("#create-btn").click(function () {

        // get user info from the ui
        var user_id = $("#user_id").val();
        var first_name = $("#first_name").val();
        var last_name = $("#last_name").val();
        var password = $("#password").val();
        var active = $("#active").val();

        // get address from the ui
        var street = $("#street").val();
        var apartment = $("#apartment").val();
        var city = $("#city").val();
        var state = $("#state").val();
        var zip_code = $("#zip_code").val();

        // create address obj
        var address = {
            "street": street,
            "apartment": apartment,
            "city": city,
            "state": state,
            "zip_code": zip_code
        }

        // create data obj
        var data = {
            "user_id": user_id,
            "first_name": first_name,
            "last_name": last_name,
            "password": password,
            "active": active,
            "address": address
        };

        // send it to the backend
        var ajax = $.ajax({
            type: "POST",
            url: "/customers",
            contentType: "application/json",
            data: JSON.stringify(data),
        });

        ajax.done(function(res){
            update_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });
    });


    // ****************************************
    // Update a Customer
    // ****************************************

    $("#update-btn").click(function () {

        var customer_id = $("#customer_id").val();
        
        var user_id = $("#user_id").val();
        var first_name = $("#first_name").val();
        var last_name = $("#last_name").val();
        var password = $("#password").val();
        var active = $("#active").val();

        // get address from the ui
        var street = $("#street").val();
        var apartment = $("#apartment").val();
        var city = $("#city").val();
        var state = $("#state").val();
        var zip_code = $("#zip_code").val();

        // create address obj
        var address = {
            "street": street,
            "apartment": apartment,
            "city": city,
            "state": state,
            "zip_code": zip_code
        }

        // create data obj
        var data = {
            "user_id": user_id,
            "first_name": first_name,
            "last_name": last_name,
            "password": password,
            "active": active,
            "address": address
        };

        var ajax = $.ajax({
                type: "PUT",
                url: "/customers/" + customer_id,
                contentType: "application/json",
                data: JSON.stringify(data)
            })

        ajax.done(function(res){
            update_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });

    });


    // ****************************************
    // Deactivate a Customer
    // ****************************************

    $("#deactivate-btn").click(function () {

        var customer_id = $("#customer_id").val();

        var ajax = $.ajax({
                type: "PUT",
                url: "/customers/" + customer_id + "/deactivate",
                contentType: "application/json"
            })

        ajax.done(function(res){
            // console.log(res)
            update_form_data(res)
            flash_message("Customer deactivated.")
            show_in_search_results_by_customer_id()
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });

    });


    // ****************************************
    // Activate a Customer
    // ****************************************

    $("#activate-btn").click(function () {

        var customer_id = $("#customer_id").val();

        var ajax = $.ajax({
                type: "PUT",
                url: "/customers/" + customer_id + "/activate",
                contentType: "application/json"
            })

        ajax.done(function(res){
            update_form_data(res)
            flash_message("Customer activated.")
            show_in_search_results_by_customer_id()
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });

    });

    // ****************************************
    // Retrieve a Customer
    // ****************************************

    $("#retrieve-btn").click(function () {
        console.log("retrieve-btn.click")
        var customer_id = $("#customer_id").val();
        var ajax = $.ajax({
            type: "GET",
            url: "/customers/" + customer_id,
            contentType: "application/json",
            data: ''
        })

        ajax.done(function(res){
            console.log("retrieve-btn.click: res")
            console.log(res)
            update_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            clear_form_data()
            flash_message(res.responseJSON.message)
        });

    });

    // ****************************************
    // Delete a Customer
    // ****************************************

    $("#delete-btn").click(function () {

        var customer_id = $("#customer_id").val();

        var ajax = $.ajax({
            type: "DELETE",
            url: "/customers/" + customer_id,
            contentType: "application/json",
            data: '',
        })

        ajax.done(function(res){
            clear_form_data()
            flash_message("Customer has been Deleted!")
        });

        ajax.fail(function(res){
            flash_message("Server error!")
        });
    });

    // ****************************************
    // Clear the form
    // ****************************************

    $("#clear-btn").click(function () {
        $("#customer_id").val("");
        clear_form_data()
    });

    // ****************************************
    // List/Query Customers
    // ****************************************

    $("#search-btn").click(function () {
        console.log("search-btn.click")
        var user_id= $("#user_id").val();
        var first_name = $("#first_name").val();
        var last_name = $("#last_name").val();
        var active = $("#active").val();
        var city = $("#city").val();
        var state = $("#state").val();
        var zip_code = $("#zip_code").val();
        var apartment = $("#apartment").val();
        var street = $("#street").val();

        var queryString = ""


        if (user_id) {
            queryString += 'user_id=' + first_name
        }
        if (first_name) {
            if (queryString.length > 0) {
                queryString += '&first_name=' + first_name
            } else {
                queryString += 'first_name=' + first_name
            }
        }
        if (last_name) {
            if (queryString.length > 0) {
                queryString += '&last_name=' + last_name
            } else {
                queryString += 'last_name=' + last_name
            }
        }
        if (active) {
            if (queryString.length > 0) {
                queryString += '&active=' + active
            } else {
                queryString += 'active=' + active
            }
        }
        if (city) {
            if (queryString.length > 0) {
                queryString += '&city=' + city
            } else {
                queryString += 'city=' + city
            }
        }
        if (state) {
            if (queryString.length > 0) {
                queryString += '&state=' + state
            } else {
                queryString += 'state=' + state
            }
        }
        if (zip_code) {
            if (queryString.length > 0) {
                queryString += '&zip_code=' + zip_code
            } else {
                queryString += 'zip_code=' + zip_code
            }
        }
        if (street) {
            if (queryString.length > 0) {
                queryString += '&street=' + zip_code
            } else {
                queryString += 'street=' + zip_code
            }
        }
        if (apartment) {
            if (queryString.length > 0) {
                queryString += '&apartment=' + zip_code
            } else {
                queryString += 'apartment=' + zip_code
            }
        }

        var ajax = $.ajax({
            type: "GET",
            url: "/customers?" + queryString,
            contentType: "application/json",
            data: ''
        })

        console.log(ajax.url)

        ajax.done(function(res){
            //alert(res.toSource())
            $("#search_results").empty();
            $("#search_results").append('<table class="table-striped" cellpadding="10">');
            var header = '<tr>'
            header += '<th style="width:5%">Customer ID</th>'
            header += '<th style="width:10%">User ID</th>'
            header += '<th style="width:15%">First Name</th>'
            header += '<th style="width:15%">Last Name</th>'
            header += '<th style="width:40%">Address</th>'
            header += '<th style="width:15%">Active</th></tr>'
            $("#search_results").append(header);
            var firstCust = "";
            for(var i = 0; i < res.length; i++) {
                var customer = res[i];
                var addr = customer.address
                var row = "<tr><td>"+customer.customer_id+"</td><td>"+customer.user_id+"</td><td>"+customer.first_name+"</td><td>"+customer.last_name+"</td><td>"+
                addr.street+", "+addr.apartment+", "+addr.city+", "+addr.state+" - "+addr.zip_code+"</td><td>"+customer.active+"</td></tr>";
                $("#search_results").append(row);
                if (i == 0) {
                    firstCust = customer;
                }
            }

            $("#search_results").append('</table>');

            // copy the first result to the form
            if (firstCust != "") {
                update_form_data(firstCust)
            }
            else {
                clear_form_data()
            }

            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });
    });
})