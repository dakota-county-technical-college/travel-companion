/* This is the main script file for Trips-R-Us */

/* JQUERY ON READY FUNCTION */
$(document).ready(function() {
    /* AUTH MODAL SCRIPT */
    const $modal = $("#authModal");
    const $modalBox = $(".modal-box");
    const $signInForm = $(".sign-in");
    const $signUpForm = $(".sign-up");

    $modal.hide();

    $("#nav-register-button").click(function () {
        $modalBox.addClass("active");
        $signInForm.hide();
        $signUpForm.show();
        $modal.show();
    });

    $("#nav-signin-button").click(function () {
        $modalBox.removeClass("active");
        $signInForm.show();
        $signUpForm.hide();
        $modal.show();
    });

    $("#register").click(function () {
        $modalBox.addClass("active");
        $signInForm.hide();
        $signUpForm.show();
    });

    $("#login").click(function () {
        $modalBox.removeClass("active");
        $signInForm.show();
        $signUpForm.hide();
    });

    $modal.click(function (event) {
        if (event.target === this) {
            console.log("I feel the click!");
            $modal.hide();
        }
    });

    /* AJAX signup script to display form errors without reloading the page */
    $("#signup-form").on("submit", function (e) {
        e.preventDefault();
        let url = $(this).data("url");
        $.ajax({
            url: url,
            type: "POST",
            data: $(this).serialize(),
            dataType: "json",
            success: function (data) {
                if (data.success) {
                    location.reload();
                } else {
                    $("#id_username_error").text(data.errors.username);
                    $("#id_email_error").text(data.errors.email);
                    $("#id_password1_error").text(data.errors.password1);
                    $("#id_password2_error").text(data.errors.password2);
                }
            },
        });
    });

    /* AJAX signup script to ensure user ends on the page they began on */
    $("#login-form").on("submit", function (e) {
        e.preventDefault();
        let url = $(this).data("url");
        $.ajax({
            url: url,
            type: "POST",
            data: $(this).serialize(),
            dataType: "json",
            success: function (data) {
                if (data.success) {
                    location.reload();
                } else {
                    console.log(data.errors);
                    $("#id_login_error").text(data.errors);
                }
            },
        });
    });
});

