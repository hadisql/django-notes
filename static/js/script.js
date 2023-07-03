const avatar = document.querySelector('#avatar')
const choosePic = document.querySelector('#choosepic')

avatar.addEventListener('click', () => {
  console.log('click avatar');

  if(choosePic.classList.contains('hidden')){ // Open avatar file choosing button
    choosePic.classList.remove('hidden');
    console.log('open choose button');
  } else {
    choosePic.classList.add('hidden');
    console.log('close choose button');
  }
});
