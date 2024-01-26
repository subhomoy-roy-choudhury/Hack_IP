$(document).ready(function () {
    const url = new URL(window.location.href);
    const params = new URLSearchParams(url.search);
    const encodedString = params.get('o');

    // Ensure the string is correctly encoded
    encodedString = decodeURIComponent(encodedString); // Decode URL encoding
    encodedString = encodedString.replace(/\s/g, '+'); // Replace spaces with '+'

    // Decode the String using built-in atob function
    let decodedString = "";
    try {
        decodedString = atob(encodedString);
        decodedString = decodedString.replace(/'/g, '"'); // Replace single quotes with double quotes if needed
    } catch (e) {
        console.error("Error decoding Base64 string", e);
    }

    let informationJson = {};
    try {
        informationJson = JSON.parse(decodedString);
    } catch (e) {
        console.error("Error parsing JSON", e);
    }

    // Render JSON in tree format
    $('#json-renderer').jsonViewer(informationJson);
    // // Display raw JSON data
    // $('#raw-json').html('<pre>' + JSON.stringify(jsonData, null, 4) + '</pre>');
    // Display Device Name
    $('#system-name').text(informationJson.system_information?.system);

    $('#downloadButton').click(function () {
        var dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(informationJson, null, 4));
        var $downloadAnchor = $('<a>', {
            href: dataStr,
            download: 'hackip-report.json'
        }).appendTo('body');

        $downloadAnchor[0].click();
        $downloadAnchor.remove();
    });
});
