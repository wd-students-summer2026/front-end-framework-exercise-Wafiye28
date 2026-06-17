// this is your custom Javascript file

$(function () {
  $(document).ready(function () {

    // CONTENT CHANGE
    $("#changeText").click(function () {

        $("#description").text(
            "Through Model United Nations, I have developed leadership, research, and communication skills while learning about international relations."
        );

    });

    // IMAGE SWAP
    $("#munImage").mouseover(function () {

        $("#munImage").attr(
            "src",
            "images/developer-8829717_960_720.jpg"
        );

    });

    $("#munImage").mouseout(function () {

        $("#munImage").attr(
            "src",
            "images/un-4984799_1280.jpg"
        );

    });

    // ANIMATION
    $("#moveBox").click(function () {

        $("#animationBox").animate({
            left: "200px",
            top: "30px"
        });

    });

});
})
