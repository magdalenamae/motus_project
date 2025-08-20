const initalMode = localStorage.getItem('mode')
console.log(initalMode)

if (initalMode == 'dark') {
 document.body.classList.add('darkmode')
} 

const darkModeButton = document.getElementById('darkmode')

darkModeButton.addEventListener('click', function() {
 console.log('toggle dark mode')
 
 // document.body.classList.toggle('darkmode');
  if (document.body.classList.contains('darkmode')) {
   document.body.classList.remove('darkmode')
   localStorage.setItem('mode', 'light')

  } else {
   document.body.classList.add('darkmode');
   localStorage.setItem('mode','dark')
  }


})



function randomPicture() {
  const randomNumber = Math.floor(Math.random() * 10)
  const randomImage = `https://picsum.photos/id/${randomNumber}/200/300`
  return randomImage
}

console.log(randomPicture())