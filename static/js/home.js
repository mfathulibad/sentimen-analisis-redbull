// Your JavaScript code goes here
function submitForm() {
    // Get form data
    var formData = new FormData(document.getElementById('addTopicForm'));
  
    // Show loading indicator
    var loadingIndicator = document.getElementById('loadingIndicator');
    loadingIndicator.style.display = 'block';
  
    // Perform AJAX request
    $.ajax({
      type: 'POST',
      url: '/form_submit',  // Use the correct URL for the Flask route
      data: formData,
      processData: false,
      contentType: false,
      success: function(response) {
        // Hide loading indicator on success
        loadingIndicator.style.display = 'none';
        // Handle the success response if needed
        console.log(response);
  
        // Update card content with input values
        var topicCardTitle = document.getElementById('topicCardTitle');
        var topicCardText = document.getElementById('topicCardText');
        var topicCardText2 = document.getElementById('topicCardText2');
  
        // Get the input values from the form
        var title = formData.get('title');
        var amount = formData.get('amount');
        var startDate = formData.get('startDate');
        var endDate = formData.get('endDate');
  
        // Format the date as needed
        var formattedDate = startDate + ' s.d.<br>' + endDate;
  
        // Get the current date in the format "dd-mm-yyyy"
        var currentDate = getCurrentDate();
  
        // Update card content
        topicCardTitle.innerHTML = title;
        topicCardText.innerHTML = formattedDate;
        topicCardText2.innerHTML = 'Total Data: ' + amount;
  
        closeModal();
      },
      error: function(error) {
        // Hide loading indicator on error
        loadingIndicator.style.display = 'none';
        // Handle the error response if needed
        console.error(error);
      }
    });
  }
  
  function deleteTopic(topicId) {
    var confirmDelete = confirm("Are you sure you want to delete this topic?");
    if (confirmDelete) {
      // Get the topicId from the data-topicid attribute
      var topicIdToDelete = event.currentTarget.getAttribute('data-topicid');
      // Print the value of topicIdToDelete
      console.log("Topic ID to delete:", topicIdToDelete);
  
      // Perform AJAX request
      $.ajax({
        type: 'POST',
        url: '/delete_topic',
        data: { topicId: topicIdToDelete },
        success: function(response) {
          // Handle success response if needed
          console.log(response);
  
          // Remove the deleted topic card from the DOM
          var topicCard = document.getElementById('topicCard' + topicIdToDelete);
          topicCard.parentNode.removeChild(topicCard);
        },
        error: function(error) {
          // Handle error response if needed
          console.error(error);
        }
      });
    }
  }
  
  function getCurrentDate() {
    var today = new Date();
    var dd = String(today.getDate()).padStart(2, '0');
    var mm = String(today.getMonth() + 1).padStart(2, '0'); // January is 0!
    var yyyy = today.getFullYear();
  
    return yyyy + '-' + mm + '-' + dd;
  }
  
  // Get the modal
  var modal = document.getElementById('addTopicModal');
  // Get the button that opens the modal
  var btn = document.getElementById("addTopicButton");
  // Get the <span> element that closes the modal
  var span = document.getElementsByClassName("close")[0];
  // When the user clicks the button, open the modal
  btn.onclick = function() {
    modal.style.display = "block";
  }
  // When the user clicks on <span> (x), close the modal
  span.onclick = function() {
    closeModal();
  }
  // When the user clicks anywhere outside of the modal, close it
  window.onclick = function(event) {
    if (event.target == modal) {
      closeModal();
    }
  }
  function closeModal() {
    modal.style.display = "none";
  }
  function saveTopic() {
    // Add logic to save the topic (e.g., get the input value and process it)
    closeModal();
  }
  function toggleTimeline() {
    var timelineFields = document.getElementById('timelineFields');
    var enableTimelineRadio = document.getElementById('enableTimeline');
    var defaultTimelineRadio = document.getElementById('defaultTimeline');
    var startDateInput = document.getElementById('startDate');
    var endDateInput = document.getElementById('endDate');
  
    if (enableTimelineRadio.checked) {
      timelineFields.style.display = 'block';
    } else {
      timelineFields.style.display = 'none';
    }
  
    // If "Default" radio is checked, hide timelineFields
    if (defaultTimelineRadio.checked) {
      // Jika "Default" radio dipilih, atur nilai startDate dan endDate satu bulan sebelumnya
      var currentDate = new Date();
      var lastMonth = new Date(currentDate);
      lastMonth.setMonth(currentDate.getMonth() - 1);
  
      // Format tanggal ke dalam format 'yyyy-mm-dd' yang diperlukan untuk input date
      var formattedLastMonth = formatDate(lastMonth);
  
      startDateInput.value = formattedLastMonth;
      endDateInput.value = formatDate(currentDate);
    }
  }
  function formatDate(date) {
    var dd = String(date.getDate()).padStart(2, '0');
    var mm = String(date.getMonth() + 1).padStart(2, '0');
    var yyyy = date.getFullYear();
    return yyyy + '-' + mm + '-' + dd;
  }
  
  document.addEventListener("DOMContentLoaded", function() {
    // Mendapatkan semua elemen dengan kelas 'topic-card'
    var topicCards = document.querySelectorAll('.topic-card');
  
    // Menambahkan event listener ke setiap elemen 'topic-card'
    topicCards.forEach(function(card) {
      card.addEventListener('click', function() {
        var topicId = this.getAttribute('data-topicid');
  
        // Mengarahkan pengguna ke hasilAnalisis.html dengan menyertakan topicId sebagai query parameter
        window.location.href = '/hasil/' + topicId;
      });
    });
  });
  