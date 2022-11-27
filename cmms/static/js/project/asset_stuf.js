$(function () {
sort_name='asc';
sort_code=1;
var asset_sort=function(){

  // alert(e);
  console.log($(this));
  // let sortDirection = $(this).sortDir || 'asc' //
  // $(this).sortDir = sortDirection == 'asc' ? 'desc' : 'asc'
  sort_type=$(this);

  // console.log(sort_type.index());
  $.ajax({
   url: '/Asset/Sort/'+sort_type.index()+'?e='+sort_type.attr('data-sort-type')+'&search='+$('#assetSearch').val()+'&kvm=0&main_asset='+$('#id_main_asset').val(),
   beforeSend: function () {

     // $("#modal-assettype").modal({backdrop: 'static', keyboard: false});
   },
   success: function (data) {
     $("#tbody_company").empty();
     $("#tbody_company").html(data.html_asset_list);
     $(".assetPaging").html(data.html_asset_paging);

     if(sort_type.attr('data-sort-type')=='asc'){
       // alert('here');
       sort_type.attr('data-sort-type','desc');

     }
     else{
       sort_type.attr('data-sort-type','asc');

     }




   }
 });
}
$("#theader_company").on("click", "th", asset_sort);
// $("#company-table ").on("click", ".js-update-asset", myWoLoader);
});
