/* Any line comment
another line */
function test_attach_click (prnt) {
    var elements = prnt.get_elements_by_tag_name("div")             // One line comment
    for(var i = 0; i < elements.length; i++) {
        elements[i].onclick = function() {
            alert("click on " + this.number)
        }
        elements[i].number = ii
    }
}

function resize (to_width, to_height, save_proportions, animate)  {
    // default value
    save_proportions = save_proportions || true
    animate = animate || true
    to_height = to_height || true
}

function is_palindrome (my_str){
    var str_len = my_str.length,
        str_reverse = my_str.split('').reverse().join('');
    if (str_reverse == my_str) {
      return "yes";
    } else {
      return "no";
    }
}

function check_age(age) {
  if (age > 18) {
    return true;
  } else {
    return confirm("Success?");
  }
}
