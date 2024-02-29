document.addEventListener("DOMContentLoaded", function() {
    document.getElementById("application-form").addEventListener("submit", function(event) {
        document.getElementById("submit").style.display = "none";
        document.getElementById("loader").style.display = "block";
    });
});

// Post creation button
$(document).ready(function() {
    // Disable the submit button to prevent double submission
    $("button[id='post-create-btn']").prop("disabled", true).css({"background-color": "#e4e6eb", "color": "#727577"});
    // Check text box content on keyup event
    $("textarea[name='post-content']").on("keyup", function() {
      // Check if the text area is empty
        if ($(this).val().trim() != "") {
            // If there is text, enable the submit button and remove styles
            $("button[id='post-create-btn']").prop("disabled", false).css({"background-color": "", "color": ""});
        }else if($(this).val().trim() === ""){
            // Disable the submit button to prevent double submission
            $("button[id='post-create-btn']").prop("disabled", true).css({"background-color": "#e4e6eb", "color": "#727577"});
        }
    });

    // Check file input for changes
    $("input[name='post-media']").on("change", function() {
        // Check if files are selected
        if ($(this).get(0).files.length > 0) {
            // If files are selected, enable the submit button and remove styles
            $("button[id='post-create-btn']").prop("disabled", false).css({"background-color": "", "color": ""});
        } else {
            // If no files are selected, disable the submit button and apply styles
            $("button[id='post-create-btn']").prop("disabled", true).css({"background-color": "#e4e6eb", "color": "#727577"});
        }
    });

    // Listen for form submission
    $("form").submit(function() {
        // Disable the submit button to prevent double submission
        $("button[id='post-create-btn']").prop("disabled", true);
        // Change button styles
        $("button[id='post-create-btn']").css({"background-color": "#e4e6eb", "color": "#727577"});
    });
});

//check if post file is other than image
$(document).ready(function() {
    // Disable the submit button initially
    $("button[id='post-create-btn']").prop("disabled", true).css({"background-color": "#e4e6eb", "color": "#727577"});

    // Check text box content on keyup event
    $("textarea[name='post-content']").on("keyup", function() {
        togglePostButton();
    });

    // Check file input for changes
    $("input[name='post-media']").on("change", function() {
        var fileInput = $(this).get(0);
        var files = fileInput.files;
        var isValid = true;

        // Check if files are selected
        if (files.length > 0) {
            for (var i = 0; i < files.length; i++) {
                var fileName = files[i].name;
                var ext = fileName.split('.').pop().toLowerCase();
                
                // Check if the file extension is allowed
                if (['png', 'jpg', 'jpeg'].indexOf(ext) === -1) {
                    isValid = false;
                    break;
                }
            }
        }

        if (!isValid) {
            // If invalid file is selected, disable the submit button and display alert
            $("button[id='post-create-btn']").prop("disabled", true).css({"background-color": "#e4e6eb", "color": "#727577"});
            Swal.fire({
                icon: "error",
                title: "Oops...",
                text: "Invalid file type. Please select only PNG, JPG, or JPEG files.",
            });
            // alert("Invalid file type. Please select only PNG, JPG, or JPEG files.");
        } else {
            // If valid files are selected, enable the submit button
            togglePostButton();
        }
    });

    // Function to toggle post button based on textarea content and file input
    function togglePostButton() {
        var hasText = $("textarea[name='post-content']").val().trim() !== "";
        var hasFiles = $("input[name='post-media']").get(0).files.length > 0;

        if (hasText || hasFiles) {
            $("button[id='post-create-btn']").prop("disabled", false).css({"background-color": "", "color": ""});
        } else {
            $("button[id='post-create-btn']").prop("disabled", true).css({"background-color": "#e4e6eb", "color": "#727577"});
        }
    }
});


// Like post logic
$(document).ready(function(){
    $(".post-meta-like").on("click", function(event){
        event.preventDefault();

        post_pk = $(this).attr("data-id");
        url = $(this).attr("data-url");
        like_count = Number($(this).attr("data-like"));
        data = {
            post_pk: post_pk,
        }

        var likeButton = $(this); // Store the like button element

        $.ajax({
            type: "GET",
            url: url,
            data: data,
            success: function(response){
                // $("#like-section").load(location.href + " #like-section");

                console.log(response);
                console.log(response.total_likes);
                console.log(like_count);

                if("total_likes" in response){
                    // Update the like count in the HTML
                    like_count++;
                    console.log(`if("total_likes" in response)`);
                    likeButton.find('#like-count').text(response.total_likes);
                }else{
                    if(like_count != 0){
                        console.log(`if(like_count != 0){`);
                        like_count--;
                        likeButton.find('#like-count').text(like_count);
                    }else if(like_count === 0){
                        console.log(`}else{`);
                        likeButton.find('#like-count').text(0);
                    }
                }

            }
        });
    });
});

// if(response.message === "DisLike Post"){
//     if(like_count === 1){
//         like_count = 0;
//         console.log(response);
//         console.log(typeof like_count);
//         console.log(like_count);    
//     }else{
//         like_count -= 1;
//         console.log(response);
//         console.log(typeof like_count);
//         console.log(like_count);
//     }
// }else if(response.message === "Like Post"){
//     like_count += 1;
//     console.log(response);
//     console.log(typeof like_count);
//     console.log(like_count);
// }


document.getElementById('copy-link-button').addEventListener('click', function() {
    var textToCopy = window.location.href;

    navigator.clipboard.writeText(textToCopy).then(function() {
        alert('Link copied to clipboard: ' + textToCopy);
    }).catch(function(err) {
        console.error('Error copying text: ', err);
    });
});
