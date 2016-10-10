$(document).ready(function(){
  if (typeof(Storage) !== "undefined") {
    // Code for localStorage/sessionStorage.
    var total = 0;
    for ( var i = 0, len = localStorage.length; i < len; ++i ) {
      console.log( localStorage.getItem( localStorage.key( i ) ) );
      var item = localStorage.getItem( localStorage.key( i ) );
      item = JSON.parse(item);
      total = total + (item['price']*item['inventory']);
      $('#cart-form').append('<input type="hidden" name=item['+i+'][name] value="'+item["name"]+'">');
      $('#cart-form').append('<input type="hidden" name=item['+i+'][price] value="'+item["price"]*item["inventory"]+'">');
      $('#cart-form').append('<input type="hidden" name=item['+i+'][quantity] value="'+item["inventory"]+'">');
      $('#cart-form').append('<input type="hidden" name=item['+i+'][product_id] value="'+item["id"]+'">');
      var html = '<tr><td>'+(i+1)+'</td><td>'+item['name']+'</td><td>'+item['price']*item['inventory']+'</td><td>'+item['inventory']+'</td></tr>';
      console.log(html);
      $('#cart_add').append(html);
    }
    $('#price').text('Rs.'+total);
  } else {
    // Sorry! No Web Storage support..
    console.log('Storage not supported');
  }
});
