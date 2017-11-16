$(function() {
  $('a#process_input').bind('click', function() {
    var id_ = $(this).attr('name');                            //return the id (from the first span), which is the index of the entry in the database
    var english_ =  document.getElementById('eng'+id_);        //Dutch word
    var res = document.getElementById('res'+id_);
    restxt = res.textContent;
    $.getJSON('/_validate', {                                  //forward the values to the python function
      id: id_,
      english: english_.value,
      res: restxt,                                             // this is the result
    }, function(data) {
      res.innerHTML = data.result;                             // Returning the result
    });
    return false;
  });
});

$(function() {
  $('a#process_all').bind('click', function() {
    var buttons = document.getElementsByName('but');             //return the id, which is the index of the entry in the database
    for(var i = 0; i <= buttons.length; i++){
       buttons[i].click();
    }
  });
});

 $(function() {
 $('a#count_').bind('click', function() {
    var childText = $('#master_').text();
    var count = (childText.match(/CORRECT/g) || []).length;
    var count2 = (childText.match(/WRONG/g) || []).length;
    alert('You got '+count+' correct and '+count2+' wrong');
    });
});
