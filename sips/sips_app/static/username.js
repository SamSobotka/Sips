function generateUsername() {
    // Get the input value
    var userInput = document.getElementById('usernameInput').value;

    // Check if the user entered a username
    if (userInput.trim() !== "") {
        // Generate a response with the username
        var response = "Hello, " + userInput + "! Your username is awesome!";

        // Redirect to the results page with the username as a query parameter
        window.location.href = "results.html?username=" + encodeURIComponent(userInput);
    } else {
        // Generate a response for an empty username
        alert("Please enter a valid username!");
    }
}