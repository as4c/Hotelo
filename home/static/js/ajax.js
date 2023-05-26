
$(document).ready(function() {
    console.log("enter in Ajax hitted")
    // Add click event listener to "Check Availability" button
      $("#check-availability-btn").click(function(e) {
          e.preventDefault();
          // Get the hotel, start date, end date, and room count values from the form (replace "..." with your code)
          var pathname = window.location.pathname;
          var parts = pathname.split('/');
          var uid = parts[2];
          var hotelId = uid
          console.log("uid :",hotelId)
          var startDate =$('#checkin').val();
          var endDate =$('#checkout').val();
          var rooms=$('#room_count').val();
          var roomType=$('#room_type').val();
          // Make an AJAX request to the backend "check_availability" function
          $.ajax({
          type:"POST",
          url: '/check_avail/',
          data: {
              "uid":hotelId,
              "check_in": startDate,
              "check_out": endDate,
              "room_count": rooms,
              "room_type":roomType,
              csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
          },
          dataType: "json",
          success: function(response) {
              console.log(response)
              if (response["available"]) {
              // Show the "Book Now" button
              $("#book-now-btn").show();
              $("#check-availability-btn").hide()
              // Hide the error message (if displayed)
              alert(response['message'])
              $("#error-msg").hide();
              } else {
              // Hide the "Book Now" button
              $("#book-now-btn").hide();
              // Show the error message
              $("#error-msg").text("Sorry, there are not enough available rooms for the selected date range and room count.").show();
              }
              $('#check_in').val('');
                $('#check_out').val('');
                $('#room_count').val('');
                $('#room_type').val('');
          },
          error: function(xhr, status, error) {
              // Display an error message
              $("#error-msg").text("An error occurred while checking room availability. Please try again later.").show();
              $('#checkin').val('');
                $('#checkout').val('');
                $('#room_count').val('');
                $('#room_type').val('');
          }
          });
          
      });
      });