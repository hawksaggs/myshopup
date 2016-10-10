// $(document).ready(function(){
  function addtocart(price,inventory,id,name)
  {
    if (typeof(Storage) !== "undefined") {
      // Code for localStorage/sessionStorage.
      var cart = {};
      var quantity  = $('#quantity_'+id).val();
      console.log(quantity);
      cart.price = price;
      cart.inventory = quantity;
      cart.id = id;
      cart.name = name;
      cart = JSON.stringify(cart);
      console.log(cart);
      localStorage.setItem(id,cart);
  } else {
      // Sorry! No Web Storage support..
      console.log('Storage not supported');
  }
}
// });
