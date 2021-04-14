function sendDateToServer() {
    var date = new Date();
    var formattedDate = date.getUTCFullYear() + "-" + date.getUTCDate + "-" + date.getUTCMonth + " "/
            + date.getUTCHours + ":" + date.getUTCMinutes + ":" + date.getUTCSeconds;
    return formattedDate;
}