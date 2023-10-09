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

       // Add autocomplete functionality using jQuery UI Autocomplete
       function setupAutocomplete(element, suggestions) {
           element.autocomplete({
               source: suggestions,
               minLength: 1, // Minimum characters to trigger autocomplete
               select: function (event, ui) {
                   $(this).closest('td').find('.create-item-link, .create-supplier-link').hide(); // Hide the "Create New" links when a suggestion is selected
               },
               response: function (event, ui) {
                   if (ui.content.length === 0) {
                       $(this).closest('td').find('.create-item-link, .create-supplier-link').show(); // Show the "Create New" links if there are no suggestions
                   } else {
                       $(this).closest('td').find('.create-item-link, .create-supplier-link').hide(); // Hide the links if suggestions are available
                   }
               }
           });
       }

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

       // Initialize autocomplete for the initial row
       setupAutocomplete($('.item-name'), itemSuggestions);
       setupAutocomplete($('.item-supplier'), supplierSuggestions);
})
