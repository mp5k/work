/* ajax通信 */
//同期ajax
function sendSync(message) {
    return $.ajax({
        url: "/send_message/" + message,
        async: false
    }).responseText;
}
