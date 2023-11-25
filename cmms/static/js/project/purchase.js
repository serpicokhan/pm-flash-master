$(function () {
  var itemSuggestions = [
           "Item 1",
           "Item 2",
           "Item 3",
           "Item 4",
           "Item 5"
       ];

       var supplierSuggestions = [
           "Supplier 1",
           "Supplier 2",
           "Supplier 3",
           "Supplier 4",
           "Supplier 5"
       ];
       function getItemSuggestions(input) {
                $.ajax({
                    url: '/get-item-suggestions', // Replace with your server endpoint URL
                    method: 'GET',
                    dataType: 'json',
                    data: { input: input }, // Send user input to the server
                    success: function(response) {
                        window.itemSuggestions = response;
                        setupAutocomplete($('.item-name'), window.itemSuggestions);
                    },
                    error: function(xhr, status, error) {
                        console.error('Error while fetching item suggestions:', error);
                        // Handle errors as needed
                    }
                });
            }

            // Function to set up autocomplete with retrieved suggestions
            function setupAutocomplete(element, suggestions) {
                element.autocomplete({
                    source: suggestions,
                    minLength: 3, // Minimum characters to trigger autocomplete
                    select: function (event, ui) {
                        $(this).closest('td').find('.create-item-link').hide();
                    },
                    response: function (event, ui) {
                        if (ui.content.length === 0) {
                            $(this).closest('td').find('.create-item-link').show();
                        } else {
                            $(this).closest('td').find('.create-item-link').hide();
                        }
                    }
                    // Other autocomplete options
                });
            }

       // Add autocomplete functionality using jQuery UI Autocomplete
       // function setupAutocomplete(element, suggestions) {
       //     element.autocomplete({
       //         source: suggestions,
       //         minLength: 1, // Minimum characters to trigger autocomplete
       //         select: function (event, ui) {
       //             $(this).closest('td').find('.create-item-link, .create-supplier-link').hide(); // Hide the "Create New" links when a suggestion is selected
       //         },
       //         response: function (event, ui) {
       //             if (ui.content.length === 0) {
       //                 $(this).closest('td').find('.create-item-link, .create-supplier-link').show(); // Show the "Create New" links if there are no suggestions
       //             } else {
       //                 $(this).closest('td').find('.create-item-link, .create-supplier-link').hide(); // Hide the links if suggestions are available
       //             }
       //         }
       //     });
       // }

       // Handle click event for "Create New Item" and "Create New Supplier" links using event delegation
       $('#item-table').on('click', '.create-item-link a, .create-supplier-link a', function(e) {
           e.preventDefault(); // Prevent the default link behavior
           const inputField = $(this).closest('td').find('input');
           const newItem = inputField.val().trim();

           if (newItem) {
               // Determine whether it's an item or supplier
               const isItem = $(this).closest('td').hasClass('item-name');
               const suggestions = isItem ? itemSuggestions : supplierSuggestions;

               // Add the new item or supplier to the respective suggestions
               suggestions.push(newItem);
               inputField.autocomplete('option', 'source', suggestions);
               inputField.val(''); // Clear the input field
               $(this).closest('td').find('.create-item-link, .create-supplier-link').hide(); // Hide the links
           }
       });

       // Add a new row when the "Enter" key is pressed in the last cell
       $('#item-table').on('keydown', '.item-supplier', function(e) {
           if (e.which === 13) {
               e.preventDefault(); // Prevent form submission
               const currentRow = $(this).closest('tr');
               const newRow = currentRow.clone();
               newRow.find('input').val(''); // Clear input values in the new row
               newRow.appendTo(currentRow.closest('tbody'));

               // Reinitialize autocomplete for the new row
               setupAutocomplete(newRow.find('.item-name'), itemSuggestions);
               setupAutocomplete(newRow.find('.item-supplier'), supplierSuggestions);
           }
       });
       function sendDataToServer() {
               var dataToSend = [];

               // Loop through each row in the table
               $('#item-table tbody tr').each(function(index, row) {
                   var rowData = {
                       name: $(row).find('.item-name').val(),
                       quantity: $(row).find('.item-quantity').val(),
                       location: $(row).find('.item-location').val(),
                       supplier: $(row).find('.item-supplier').val()
                   };
                   dataToSend.push(rowData);
               });

               // AJAX POST request to send data to the server
               $.ajax({
                   url: '/your-server-endpoint-url', // Replace with your server endpoint URL
                   method: 'POST',
                   data: JSON.stringify(dataToSend),
                   contentType: 'application/json',
                   success: function(response) {
                       // Handle success response from the server
                       console.log('Data successfully sent to the server:', response);
                       // Perform any other actions upon success
                   },
                   error: function(xhr, status, error) {
                       // Handle error response from the server
                       console.error('Error while sending data:', error);
                       // Perform any other actions upon error
                   }
               });
           }

           // Click event handler for the "ذخیره" (Save) button
           $('.js-create-maintenanceType').on('click', function() {
               sendDataToServer(); // Call the function to send data when the button is clicked
           });
       });

       // Initialize autocomplete for the initial row
       setupAutocomplete($('.item-name'), itemSuggestions);
       setupAutocomplete($('.item-supplier'), supplierSuggestions);
})
