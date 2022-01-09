function changeColor(color) {
    document.getElementById("demo").style.background = color;
    document.getElementById("demo").innerHTML = "Joined!";
    membersIncrease()
}
function membersIncrease() {
    current_value = document.getElementById("demo1").nodeValue
    document.getElementById("demo1").innerHTML = current_value+1;
}
