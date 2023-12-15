// Get the username from the query parameter
var urlParams = new URLSearchParams(window.location.search);
var username = urlParams.get('username');

// Display the username on the page
document.getElementById('output').textContent = "Username: " + username;
