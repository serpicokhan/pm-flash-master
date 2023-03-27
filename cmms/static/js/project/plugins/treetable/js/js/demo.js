/* This is an echo of some data sent back via ajax                       */
/* This data should be filtered by nodeID and return only childNodeID's. */
/* vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv. */
var jsonData = {
  
};
/* ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ */
/* This is an echo of some data sent back via ajax                       */
/* This data should be filtered by nodeID and return only childNodeID's. */



// initialize treeTable
$("#example-basic").treetable({
    expandable:     true,
    onNodeExpand:   nodeExpand,
    onNodeCollapse: nodeCollapse
});


// expand node with ID "1" by default
$("#example-basic").treetable("reveal", '1');


// Highlight a row when selected
$("#example-basic tbody").on("mousedown", "tr", function() {
    $(".selected").not(this).removeClass("selected");
    $(this).toggleClass("selected");
});

function nodeExpand () {
    // alert("Expanded: " + this.id);
  	getNodeViaAjax(this.id);  
}


function nodeCollapse () {
    // alert("Collapsed: " + this.id);
}







function getNodeViaAjax(parentNodeID) {
    $("#loadingImage").show();
    
    // ajax should be modified to only get childNode data from selected nodeID
    // was created this way to work in jsFiddle
    $.ajax({
		type: 'POST',
        url: '/echo/json/',
        data: {
            json: JSON.stringify( jsonData )
        },
        success: function(data) {
            $("#loadingImage").hide();
    
            var childNodes = data.nodeID[parentNodeID];
            
            if(childNodes) {
                var parentNode = $("#example-basic").treetable("node", parentNodeID);

                for (var i = 0; i < childNodes.length; i++) {
                    var node = childNodes[i];

                    var nodeToAdd = $("#example-basic").treetable("node",node['ID']);

                    // check if node already exists. If not add row to parent node
                    if(!nodeToAdd) {
                        // create row to add
                        var row ='<tr data-tt-id="' + 
                            node['ID'] + 
                            '" data-tt-parent-id="' +
                            parentNodeID + '" ';
                        if(node['childNodeType'] == 'branch') {
                            row += ' data-tt-branch="true" ';
                        }

                        row += ' >';

                        // Add columns to row
                        for (var index in node['childData']) {
                            var data = node['childData'][index];
                            row += "<td>" + data + "</td>";
                        }

                        // End row
                        row +="</tr>";
                        
                        $("#example-basic").treetable("loadBranch", parentNode, row);
                    }



                }
            
            }

        },
        error:function(error){
            $("#loadingImage").hide();
            alert('there was an error');  
        },
        dataType: 'json'
    });
}

