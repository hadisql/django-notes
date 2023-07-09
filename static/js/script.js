
if (window.location.pathname === profileUpdateUrl) {

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
}



console.log('hello world')
const alertBox = document.getElementById('alert-box')
const imageBox = document.getElementById('image-box')
const imageForm = document.getElementById('image-form')
const confirmBtn = document.getElementById('confirm-btn')
const input = document.getElementById('id_file')

const csrf = document.getElementsByName('csrfmiddlewaretoken')

input.addEventListener('change', ()=>{
    alertBox.innerHTML = ""
    confirmBtn.classList.remove('hidden')
    const img_data = input.files[0]
    const url = URL.createObjectURL(img_data)

    imageBox.innerHTML = `<img src="${url}" id="image" width="700px">`
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
            fd.append('file', blob, 'my-image.png');

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
})
