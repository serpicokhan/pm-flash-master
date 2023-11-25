$(function () {
  var itemSuggestions = [

       ];
  var locationSuggestions = [

       ];

       var supplierSuggestions = [

       ];
       function getItemSuggestions(input) {
                $.ajax({
                    url: '/WoPart/GetParts', // Replace with your server endpoint URL
                    method: 'GET',
                    dataType: 'json',
                    data: { qry: input }, // Send user input to the server
                    beforeSend:function(){

                    },
                    success: function(response) {

                        window.itemSuggestions = response;
                        console.log(  window.itemSuggestions);

                        setupAutocomplete($('.item-name'), window.itemSuggestions);
                    },
                    error: function(xhr, status, error) {
                        console.error('Error while fetching item suggestions:', error);
                        // Handle errors as needed
                    }
                });
            }
       function getLocationSuggestions(input) {
                $.ajax({
                    url: '/Asset/Names', // Replace with your server endpoint URL
                    method: 'GET',
                    dataType: 'json',
                    data: { qry: input }, // Send user input to the server
                    beforeSend:function(){

                    },
                    success: function(response) {

                        window.locationSuggestions = response;
                        console.log(  window.locationSuggestions);

                        setupLocationAutocomplete($('.item-location'), window.locationSuggestions);
                    },
                    error: function(xhr, status, error) {
                        console.error('Error while fetching item suggestions:', error);
                        // Handle errors as needed
                    }
                });
            }
       function getSupplierSuggestions(input) {
                $.ajax({
                    url: '/Business/GetNames', // Replace with your server endpoint URL
                    method: 'GET',
                    dataType: 'json',
                    data: { qry: input }, // Send user input to the server
                    beforeSend:function(){

                    },
                    success: function(response) {

                        window.supplierSuggestions = response;
                        setupSupplierAutocomplete($('.item-supplier'), window.supplierSuggestions);
                    },
                    error: function(xhr, status, error) {
                        console.error('Error while fetching item suggestions:', error);
                        // Handle errors as needed
                    }
                });
            }
            function setupLocationAutocomplete(element, suggestions) {
               element.autocomplete({
                   source: function(request, response) {
                       var filtered = $.grep(suggestions, function(item) {
                           return item.assetName.toLowerCase().indexOf(request.term.toLowerCase()) >= 0;
                       });
                       response(filtered.slice(0, 10)); // Display only the first 10 matches
                   },
                   minLength: 3,
                   select: function (event, ui) {
                       $(this).val(ui.item.assetName);
                       $(this).closest('td').find('.location-id').val(ui.item.id); // Set item ID to hidden input
                       $(this).closest('td').find('.create-location-link').hide();
                       return false;
                   },
                   response: function (event, ui) {
                       if (ui.content.length === 0) {
                           $(this).closest('td').find('.create-location-link').show();
                           $(this).closest('td').find('.location-id').val(0);
                       } else {
                         $(this).closest('td').find('.location-id').val(0);

                           $(this).closest('td').find('.create-location-link').hide();
                       }
                   }
                   // Other autocomplete options
               }).data('ui-autocomplete')._renderItem = function(ul, item) {
                   return $('<li>')
                       .append('<div>' + item.assetName + '</div>')
                       .appendTo(ul);
               };
           }
            function setupAutocomplete(element, suggestions) {
               element.autocomplete({
                   source: function(request, response) {
                       var filtered = $.grep(suggestions, function(item) {
                           return item.partName.toLowerCase().indexOf(request.term.toLowerCase()) >= 0;
                       });
                       response(filtered.slice(0, 10)); // Display only the first 10 matches
                   },
                   minLength: 3,
                   select: function (event, ui) {
                       $(this).val(ui.item.partName);
                       $(this).closest('td').find('.item-id').val(ui.item.id); // Set item ID to hidden input
                       $(this).closest('td').find('.create-item-link').hide();
                       return false;
                   },
                   response: function (event, ui) {
                       if (ui.content.length === 0) {
                           $(this).closest('td').find('.create-item-link').show();
                           $(this).closest('td').find('.item-id').val(0);
                       } else {
                         $(this).closest('td').find('.item-id').val(0);

                           $(this).closest('td').find('.create-item-link').hide();
                       }
                   }
                   // Other autocomplete options
               }).data('ui-autocomplete')._renderItem = function(ul, item) {
                   return $('<li>')
                       .append('<div>' + item.partName + '</div>')
                       .appendTo(ul);
               };
           }
            function setupSupplierAutocomplete(element, suggestions) {
               element.autocomplete({
                   source: function(request, response) {
                       var filtered = $.grep(suggestions, function(item) {
                           return item.name.toLowerCase().indexOf(request.term.toLowerCase()) >= 0;
                       });
                       response(filtered.slice(0, 10)); // Display only the first 10 matches
                   },
                   minLength: 3,
                   select: function (event, ui) {
                       $(this).val(ui.item.name);
                       $(this).closest('td').find('.supplier-id').val(ui.item.id); // Set item ID to hidden input
                       $(this).closest('td').find('.create-supplier-link').hide();
                       return false;
                   },
                   response: function (event, ui) {
                       if (ui.content.length === 0) {
                           $(this).closest('td').find('.create-supplier-link').show();
                           $(this).closest('td').find('.supplier-id').val(0);
                       } else {
                         $(this).closest('td').find('.supplier-id').val(0);

                           $(this).closest('td').find('.create-supplier-link').hide();
                       }
                   }
                   // Other autocomplete options
               }).data('ui-autocomplete')._renderItem = function(ul, item) {
                   return $('<li>')
                       .append('<div>' + item.name + '</div>')
                       .appendTo(ul);
               };
           }

            // Function to set up autocomplete with retrieved suggestions
            // function setupAutocomplete(element, suggestions) {
            //     element.autocomplete({
            //         source: suggestions,
            //         minLength: 3, // Minimum characters to trigger autocomplete
            //         select: function (event, ui) {
            //             $(this).closest('td').find('.create-item-link').hide();
            //         },
            //         response: function (event, ui) {
            //             if (ui.content.length === 0) {
            //                 $(this).closest('td').find('.create-item-link').show();
            //             } else {
            //                 $(this).closest('td').find('.create-item-link').hide();
            //             }
            //         }
            //         // Other autocomplete options
            //     });
            // }

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
               setupAutocomplete(newRow.find('.item-name'), window.itemSuggestions);
               setupSupplierAutocomplete(newRow.find('.item-supplier'), window.supplierSuggestions);
               // setupAutocomplete(newRow.find('.item-supplier'), supplierSuggestions);
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
           $('.item-name').on('input', function() {
               var input = $(this).val().trim();
               if (input.length >= 3) {
                   getItemSuggestions(input);
               }
           });
           $('.item-supplier').on('input', function() {
               var input = $(this).val().trim();
               if (input.length >= 3) {
                   getSupplierSuggestions(input);
               }
           });
           $('.item-location').on('input', function() {
               var input = $(this).val().trim();

               if (input.length >= 3) {
                   getLocationSuggestions(input);
               }
           });


       // Initialize autocomplete for the initial row
       // setupAutocomplete($('.item-name'), itemSuggestions);
       // setupAutocomplete($('.item-supplier'), supplierSuggestions);
});
