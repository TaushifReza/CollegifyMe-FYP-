document.addEventListener("DOMContentLoaded", function() {
    document.getElementById("application-form").addEventListener("submit", function(event) {
        document.getElementById("submit").style.display = "none";
        document.getElementById("loader").style.display = "block";
    });
});