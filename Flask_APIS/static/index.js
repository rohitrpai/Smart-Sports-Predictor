$( document ).ready(function() {
    $(".btnPredict").click(function(){
        $(".predictText").text("Sunrisers Hyderabad")
    });

    $("#input-image").change(function() {
        // $("#changedImg").attr('src', '/img/no_preview.png');
    });

    $('select').change(function() {
        var selectedOption = $(this).find("option:selected").text()
        $(this).siblings('select').find('option').attr('disabled', false);
        $(this).siblings('select').find('option:contains(' + selectedOption + ')').attr('disabled',true);
    });
});
