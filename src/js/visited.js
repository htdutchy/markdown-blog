// Hacked implementation of :visited
// Credit: http://joelcalifa.com/blog/revisiting-visited
localStorage.setItem('visited-' + window.location.pathname, true);
var elements = document.getElementsByClassName('visited');
for (var i = 0; i < elements.length; i++) {
    var element = elements[i];
    if (localStorage.getItem('visited-' + element.dataset.url)) {
        element.dataset.visited = true;
    }
}
