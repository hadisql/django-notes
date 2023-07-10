// Nav Bar Hamburger Menu
const btnHamburger = document.querySelector('#btnHamburger');
const menu = document.querySelector('#menu');
const span1 = document.getElementById('span1');
const span2 = document.getElementById('span2');
const span3 = document.getElementById('span3');

btnHamburger.addEventListener('click', () => {
  console.log('click hamburger');

  if(menu.classList.contains('hidden')){ // Open Hamburger Menu Toggle
    menu.classList.remove('hidden');
    span1.classList.add('open-span1');
    span2.classList.add('open-span2');
    span3.classList.add('open-span3');
    console.log('open hamburger');
  } else {
    menu.classList.add('hidden');
    span1.classList.remove('open-span1');
    span2.classList.remove('open-span2');
    span3.classList.remove('open-span3');
    console.log('close hamburger');
  }
});


// Profile Update Avatar
if (window.location.pathname === profileUpdateUrl) {

  const avatar = document.querySelector('#avatar')
  const choosePic = document.querySelector('#choosepic_menu')

  const newPicButton = document.querySelector('#newpic_button')
  const newPicDiv = document.querySelector('#newpic_div')

  const prevPicButton = document.querySelector('#prevpic_button')
  const prevPicDiv = document.querySelector('#prevpic_div')

  avatar.addEventListener('click', () => {
    console.log('click avatar');

    if(choosePic.classList.contains('hidden')){ // Open avatar change menu
      choosePic.classList.remove('hidden');
      console.log('open choose button');
    } else {
      choosePic.classList.add('hidden');
      console.log('close choose button');
    }
  });

  newPicButton.addEventListener('click', () => {
    console.log('click upload avatar');

    if(newPicDiv.classList.contains('hidden')){ // Open upload new avatar file choosing button
      newPicDiv.classList.remove('hidden');
      console.log('open new avatar input');
    } else {
      newPicDiv.classList.add('hidden');
      console.log('close new avatar input');
    }
  });

  prevPicButton.addEventListener('click', () => {
    console.log('click upload avatar');

    if(prevPicDiv.classList.contains('hidden')){ // Open upload new avatar file choosing button
      prevPicDiv.classList.remove('hidden');
      console.log('open previous avatar input');
    } else {
      prevPicDiv.classList.add('hidden');
      console.log('close previous avatar input');
    }
  });
}



// CROP FUNCTIONALITY
else {

  console.log('hello world')
  const alertBox = document.getElementById('alert-box')
  const imageBox = document.getElementById('image-box')
  const imageForm = document.getElementById('image-form')
  const confirmBtn = document.getElementById('confirm-btn')
  const input = document.getElementById('id_file')

  const csrf = document.getElementsByName('csrfmiddlewaretoken')


  alertBox.innerHTML = ""
  // confirmBtn.classList.remove('hidden')
  // const img_data = input.files[0]
  //const url = document.getElementsByTagName('a')[4].href

  let url;
  const anchorElements = document.querySelectorAll("a[href*='images/avatars/']");

  anchorElements.forEach((anchorElement) => {
    const href = anchorElement.getAttribute('href');
    if (href.includes("images/avatars/")) {
      console.log(href); // Output the href value of each matching anchor element
      url = href;
    }
  });


  imageBox.innerHTML = `<img src="${url}" id="image" width="400px">`
  var $image = $('#image')
  console.log($image)

  $image.cropper({
      aspectRatio: 9 / 9,
      crop: function(event) {
          console.log(event.detail.x);
          console.log(event.detail.y);
          console.log(event.detail.width);
          console.log(event.detail.height);
          console.log(event.detail.rotate);
          console.log(event.detail.scaleX);
          console.log(event.detail.scaleY);
      }
  });

  var cropper = $image.data('cropper');
  confirmBtn.addEventListener('click', ()=>{
      cropper.getCroppedCanvas().toBlob((blob) => {
          console.log('confirmed')
          const fd = new FormData();
          fd.append('csrfmiddlewaretoken', csrf[0].value)
          fd.append('avatar', blob, 'my-image.png');

          $.ajax({
              type:'POST',
              url: imageForm.action,
              enctype: 'multipart/form-data',
              data: fd,
              success: function(response){
                  console.log('success', response)
                  alertBox.innerHTML = `<div class="my-6 px-6 py-4 bg-lime-800 border-4 border-lime-200 text-lime-200 rounded-xl text-center" role="alert">
                                          Successfully saved and cropped the selected image
                                      </div>`
              },
              error: function(error){
                  console.log('error', error)
                  alertBox.innerHTML = `<div class="my-6 px-6 py-4 bg-red-800 border-4 border-red-200 text-red-200 rounded-xl text-center" role="alert">
                                          Ups...something went wrong
                                      </div>`
              },
              cache: false,
              contentType: false,
              processData: false,
          })
      })
  })
  }
