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
    $("#street").val(addr.street);
    $("#apartment").val(addr.apartment);
    $("#city").val(addr.city);
    $("#state").val(addr.state);
    $("#zip_code").val(addr.zip_code);
    if (res.active === true) {
      $("#active").val("true").change();
    } else {
      $("#active").val("false").change();
    }
  }

  // Clears all form fields
  function clear_form_data() {
    $("#customer_id").val();
    $("#user_id").val("");
    $("#first_name").val("");
    $("#last_name").val("");
    $("#password").val("");
    $("#street").val("");
    $("#apartment").val("");
    $("#city").val("");
    $("#state").val("");
    $("#zip_code").val("");
    $("#active").val("n/a").change();
  }

  // Updates the flash message area
  function flash_message(message) {
    $("#flash-message").empty();
    $("#flash-message").append(message);
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
    var active = $("#active").val() == "true";

    // get address from the ui
    var street = $("#street").val();
    var apartment = $("#apartment").val();
    var city = $("#city").val();
    var state = $("#state").val();
    var zip_code = $("#zip_code").val();

    // create address obj
    var address = {};
    street && (address.street = street);
    apartment && (address.apartment = apartment);
    city && (address.city = city);
    state && (address.state = state);
    zip_code && (address.zip_code = zip_code);

    // create customer obj
    var customer = {};
    user_id && (customer.user_id = user_id);
    first_name && (customer.first_name = first_name);
    last_name && (customer.last_name = last_name);
    password && (customer.password = password);
    active !== "n/a" && (customer.active = active);
    address && (customer.address = address);

    // send it to the backend
    var ajax = $.ajax({
      type: "POST",
      url: "api/customers",
      contentType: "application/json",
      data: JSON.stringify(customer),
    });

    ajax.done(function (res) {
      update_form_data(res);
      flash_message("Success");
    });

    ajax.fail(function (res) {
      flash_message(res.responseJSON.message);
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
    var active = $("#active").val() == "true";

    // get address from the ui
    var street = $("#street").val();
    var apartment = $("#apartment").val();
    var city = $("#city").val();
    var state = $("#state").val();
    var zip_code = $("#zip_code").val();

    // create address obj
    var address = {};
    street && (address.street = street);
    apartment && (address.apartment = apartment);
    city && (address.city = city);
    state && (address.state = state);
    zip_code && (address.zip_code = zip_code);

    // create customer obj
    var customer = {};
    customer_id && (customer.customer_id = customer_id)
    user_id && (customer.user_id = user_id);
    first_name && (customer.first_name = first_name);
    last_name && (customer.last_name = last_name);
    password && (customer.password = password);
    active !== "n/a" && (customer.active = active);
    address && (customer.address = address);

    var ajax = $.ajax({
      type: "PUT",
      url: "api/customers/" + customer_id,
      contentType: "application/json",
      data: JSON.stringify(customer),
    });

    ajax.done(function (res) {
      update_form_data(res);
      flash_message("Success");
    });

    ajax.fail(function (res) {
      flash_message(res.responseJSON.message);
    });
  });

  // ****************************************
  // Deactivate a Customer
  // ****************************************

  $("#deactivate-btn").click(function () {
    var customer_id = $("#customer_id").val();

    var ajax = $.ajax({
      type: "PUT",
      url: "api/customers/" + customer_id + "/deactivate",
      contentType: "application/json",
    });

    ajax.done(function (res) {
      // console.log(res)
      update_form_data(res);
      flash_message("Success");
    });

    ajax.fail(function (res) {
      flash_message(res.responseJSON.message);
    });
  });

  // ****************************************
  // Activate a Customer
  // ****************************************

  $("#activate-btn").click(function () {
    var customer_id = $("#customer_id").val();

    var ajax = $.ajax({
      type: "PUT",
      url: "api/customers/" + customer_id + "/activate",
      contentType: "application/json",
    });

    ajax.done(function (res) {
      update_form_data(res);
      flash_message("Success");
    });

    ajax.fail(function (res) {
      flash_message(res.responseJSON.message);
    });
  });

  // ****************************************
  // Retrieve a Customer
  // ****************************************

  $("#retrieve-btn").click(function () {
    var customer_id = $("#customer_id").val();

    var ajax = $.ajax({
      type: "GET",
      url: "api/customers/" + customer_id,
      contentType: "application/json",
      data: "",
    });

    ajax.done(function (res) {
      console.log("retrieve-btn.click: res");
      console.log(res);
      update_form_data(res);
      flash_message("Success");
    });

    ajax.fail(function (res) {
      clear_form_data();
      flash_message(res.responseJSON.message);
    });
  });

  // ****************************************
  // Delete a Customer
  // ****************************************

  $("#delete-btn").click(function () {
    var customer_id = $("#customer_id").val();

    var ajax = $.ajax({
      type: "DELETE",
      url: "api/customers/" + customer_id,
      contentType: "application/json",
      data: "",
    });

    ajax.done(function (res) {
      clear_form_data();
      flash_message("Success");
    });

    ajax.fail(function (res) {
      flash_message(res.responseJSON.message);
    });
  });

  // ****************************************
  // Clear the form
  // ****************************************

  $("#clear-btn").click(function () {
    clear_form_data();
  });

  // ****************************************
  // List/Query Customers
  // ****************************************

  $("#search-btn").click(function () {
    console.log("search-btn.click");
    var user_id = $("#user_id").val();
    var first_name = $("#first_name").val();
    var last_name = $("#last_name").val();
    var city = $("#city").val();
    var state = $("#state").val();
    var zip_code = $("#zip_code").val();
    var apartment = $("#apartment").val();
    var street = $("#street").val();
    var active = $("#active").val();

    var queryString = "";

    if (user_id) {
      queryString += "user_id=" + user_id;
    }
    if (first_name) {
      if (queryString.length > 0) {
        queryString += "&first_name=" + first_name;
      } else {
        queryString += "first_name=" + first_name;
      }
    }
    if (last_name) {
      if (queryString.length > 0) {
        queryString += "&last_name=" + last_name;
      } else {
        queryString += "last_name=" + last_name;
      }
    }
    if (city) {
      if (queryString.length > 0) {
        queryString += "&city=" + city;
      } else {
        queryString += "city=" + city;
      }
    }
    if (state) {
      if (queryString.length > 0) {
        queryString += "&state=" + state;
      } else {
        queryString += "state=" + state;
      }
    }
    if (zip_code) {
      if (queryString.length > 0) {
        queryString += "&zip_code=" + zip_code;
      } else {
        queryString += "zip_code=" + zip_code;
      }
    }
    if (street) {
      if (queryString.length > 0) {
        queryString += "&street=" + zip_code;
      } else {
        queryString += "street=" + zip_code;
      }
    }
    if (apartment) {
      if (queryString.length > 0) {
        queryString += "&apartment=" + zip_code;
      } else {
        queryString += "apartment=" + zip_code;
      }
    }
    if (active !== "n/a") {
      if (queryString.length > 0) {
        queryString += "&active=" + active;
      } else {
        queryString += "active=" + active;
      }
    }

    var ajax = $.ajax({
      type: "GET",
      url: "api/customers?" + queryString,
      contentType: "application/json",
      data: "",
    });

    console.log(ajax.url);

    ajax.done(function (res) {
      //alert(res.toSource())
      $("#search-results").empty();
      var firstCust = "";
      for (var i = 0; i < res.length; i++) {
        var customer = res[i];
        var addr = customer.address;
        var row =
          "<tr><td>" +
          customer.customer_id +
          "</td><td>" +
          customer.user_id +
          "</td><td>" +
          customer.first_name +
          "</td><td>" +
          customer.last_name +
          "</td><td>" +
          addr.street +
          ", " +
          addr.apartment +
          ", " +
          addr.city +
          ", " +
          addr.state +
          " - " +
          addr.zip_code +
          "</td><td>" +
          customer.active +
          "</td></tr>";
        $("#search-results").append(row);
        if (i == 0) {
          firstCust = customer;
        }
      }

      // copy the first result to the form
      if (firstCust != "") {
        update_form_data(firstCust);
      } else {
        clear_form_data();
      }

      flash_message("Success");
    });

    ajax.fail(function (res) {
      flash_message(res.responseJSON.message);
    });
  });
});
