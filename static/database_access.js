// Request new data from server using GET, process data
function getNewData(handleData) {
  $.ajax({
    url: "/update",
    type: "get",
    data: {},
    dataType: "json",
    success: function(response) {
      console.log(response);
      var array = [];
      for (var i in response) {
        var item = response[i];
        var row = {
          'id': item[0],
          'timestamp': item[1],
          'amount': item[2],
          'current_bal': item[3]
        };
        item.push(row);
      }
      handleData(response)
    }
  });
}

// Update the values on each page
function updatePage() {
  getNewData(function(data) {
    if (Array.isArray(data) && data.length > 0) {
      var reverseData = data.reverse();

      for (var item in reverseData) {
        var row = reverseData[item];

        // Add data to table
        $("<tr>" +
            "<td>" + row[1] + "</td>" +
            "<td>$" + row[2].toFixed(2) + "</td>" +
            "<td>$" + row[3].toFixed(2) + "</td>" +
          "</tr>").prependTo($("#tbody_transactions"));

        // Update current balance
        $("#balance").text("Curent Balance: $" + row[3].toFixed(2));
      }
    }
  });
}

// Check for new data every 3000 ms (3 seconds)
$(document).ready(function() {
  updatePage()
  setInterval(updatePage , 3000);
});