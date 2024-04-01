/* This is the main script file for Trips-R-Us */

/* JQUERY ON READY FUNCTION */
$(document).ready(function() {

    /* AUTH MODAL SCRIPT */
    const $modal = $('#authModal');
    const $modalBox = $('.modal-box');
    const $signInForm = $('.sign-in');
    const $signUpForm = $('.sign-up');

    $modal.hide();

    $('#nav-register-button').click(function() {
        $modalBox.addClass('active');
        $signInForm.hide();
        $signUpForm.show();
        $modal.show();
    });

    $('#nav-signin-button').click(function() {
        $modalBox.removeClass('active');
        $signInForm.show();
        $signUpForm.hide();
        $modal.show();
    });

    $('#register').click(function() {
        $modalBox.addClass('active');
        $signInForm.hide();
        $signUpForm.show();
    });

    $('#login').click(function() {
        $modalBox.removeClass('active');
        $signInForm.show();
        $signUpForm.hide();
    })

    $modal.click(function(event) {
        if(event.target === this) {
            console.log("I feel the click!")
            $modal.hide();
        }
    });
});

