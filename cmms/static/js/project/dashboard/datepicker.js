
  var gDashDate1=new Date();
  var gDashDate2=new Date();

  $('#dashboardt1').pDatepicker({
                  format: 'YYYY-MM-DD',
                  autoClose: true,
                  initialValueType: 'gregorian',
                  "onSelect": function(time) {
                      gDashDate1 = new persianDate(time).toDate();
                      console.log(gDashDate1);
                  }

              });
  $('#dashboardt2').pDatepicker({
                              format: 'YYYY-MM-DD',
                              autoClose: true,
                              initialValueType: 'gregorian',
                              "onSelect": function(time) {
                                  gDashDate2 = new persianDate(time).toDate();
                                  console.log(gDashDate2);
                              }

                          });
