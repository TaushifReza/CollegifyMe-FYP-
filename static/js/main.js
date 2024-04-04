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

    // Disable the submit button to prevent double submission
    $("button[id='comment-create-btn']").prop("disabled", true).css({"background-color": "#e4e6eb", "color": "#727577"});
    // Check text box content on keyup event
    $("textarea[name='comment-content']").on("keyup", function() {
      // Check if the text area is empty
        if ($(this).val().trim() != "") {
            // If there is text, enable the submit button and remove styles
            $("button[id='comment-create-btn']").prop("disabled", false).css({"background-color": "", "color": ""});
        }else if($(this).val().trim() === ""){
            // Disable the submit button to prevent double submission
            $("button[id='comment-create-btn']").prop("disabled", true).css({"background-color": "#e4e6eb", "color": "#727577"});
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

$(document).ready(function(){
    $("#post-form").submit(function(event) {
        event.preventDefault();
        // Fetch form data using FormData
        var formData = new FormData($(this)[0]);
        // Get the CSRF token value
        var csrfToken = $("input[name='csrfmiddlewaretoken']").val();
        // Add the CSRF token to the FormData object
        formData.append('csrfmiddlewaretoken', csrfToken);

        // Make an AJAX request to submit the form data
        $.ajax({
            type: "POST",
            url: $(this).attr("action"),
            data: formData,
            processData: false, // Prevent jQuery from automatically processing the data
            contentType: false, // Prevent jQuery from setting the contentType
            success: function(response){
                console.log(response);
                document.getElementById("post-form").reset();
                location.reload();
            },
            error: function(xhr, status, error) {
            // Display error message or handle errors
            console.error(xhr.responseText);
            alert("An error occurred while creating the post. Please try again later.");
        },
        });
    });
// comment logic here
$(".comment-form").submit(function(event) {
        $("button[id='comment-create-btn']").prop("disabled", true).css({"background-color": "#e4e6eb", "color": "#727577"});
        event.preventDefault();
        var formData = new FormData($(this)[0]);
        var csrfToken = $("input[name='csrfmiddlewaretoken']").val();
        formData.append('csrfmiddlewaretoken', csrfToken);
        $.ajax({
            type: "POST",
            url: $(this).attr("action"),
            data: formData,
            processData: false,
            contentType: false,
            success: function(response){
                console.log(response);
                $(".comment-form").trigger("reset");
                // location.reload();
            },
            error: function(xhr, status, error) {
            console.error(xhr.responseText);
            alert("An error occurred while creating the post. Please try again later.");
        },
        });
    });
});
// Get comment of the post logic
$(document).ready(function() {
    $(".post-comment").click(function(event) {
        event.preventDefault();
        var targetAttribute = $(this).data("bs-target");
        var postPk = targetAttribute.split("-")[1];
        $.ajax({
            type: "GET",
            url: "/get_comment_post/" + postPk + "/",
            dataType: "json",
            success: function(response) {
                console.log(response);
                var $modalBody = $("#comment-body-"+postPk);

                var commentData = response.comment_data;
                console.log(commentData.length);

                if (commentData.length === 0) {
                    var noCommentHTML = '<div class="text-center">No comments for this post</div>';
                    $modalBody.html(noCommentHTML);
                } else {
                    $modalBody.empty();
                    $.each(commentData, function(index, comment) {
                        var commentHTML = `
                            <div class="post-title d-flex align-items-center mb-2">
                                <div class="profile-thumb">
                                    <a href="#">
                                        <figure class="profile-thumb-middle">
                                            <img src="${comment.profile_image_url}" alt="profile picture" />
                                        </figure>
                                    </a>
                                </div>
                                <div class="posted-author w-100 p-3 rounded" style="background-color: #f0f2f5;">
                                    <h6 class="author">
                                        <a>${comment.user_full_name}</a>
                                    </h6>
                                    <span class="post-time">${comment.comment_content}</span>
                                </div>
                            </div>
                        `;
                        $modalBody.append(commentHTML);
                    });
                }
            },
            error: function(xhr, status, error) {
                console.error(error);
            }
        });
    });
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

// PROFILE SECTION JS

// Scroll to top when the anchor tag is clicked
document.addEventListener('DOMContentLoaded', function() {
    var scrollToTopButton = document.getElementById('scrollToTop');

    // Smooth scroll function
    function scrollToTop() {
        var startPosition = window.pageYOffset;
        var targetPosition = 0;
        var distance = targetPosition - startPosition;
        var startTime = null;
        var duration = 1000; // Duration of the scroll animation in milliseconds

        function animation(currentTime) {
            if (startTime === null) startTime = currentTime;
            var timeElapsed = currentTime - startTime;
            var run = ease(timeElapsed, startPosition, distance, duration);
            window.scrollTo(0, run);
            if (timeElapsed < duration) requestAnimationFrame(animation);
        }

        function ease(t, b, c, d) {
            t /= d / 2;
            if (t < 1) return c / 2 * t * t + b;
            t--;
            return -c / 2 * (t * (t - 2) - 1) + b;
        }

        requestAnimationFrame(animation);
    }

    scrollToTopButton.addEventListener('click', function(event) {
        event.preventDefault();
        scrollToTop();
    });
});
