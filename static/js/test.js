



$("#goToImageBtn").on("click", function() {
    var go = $("#go").val();
    var target = "#img"+go
    window.location.href = target;
});


var zoomLevel = 0;

function zoom() {
    if (clickedImageId) {
        var targetImage = $("#" + clickedImageId);
        
        if (targetImage.length) {
            zoomLevel++;
            var zoomClass = "zoom-" + zoomLevel;
            targetImage.addClass(zoomClass);
        }
    }
}

function zoomOut() {
    if (clickedImageId) {
        var targetImage = $("#" + clickedImageId);
        
        if (targetImage.length) {
            var zoomClass = "zoom-" + zoomLevel;
            targetImage.removeClass(zoomClass);
            zoomLevel--;
        }
    }
}