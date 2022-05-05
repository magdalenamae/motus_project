const darkModeButton = document.getElementById('darkmode');

darkModeButton.addEventListener('click', function(e) {
 console.log('toggle dark mode')

 document.body.classList.add('darkmode');

})