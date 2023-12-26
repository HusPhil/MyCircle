const alertBoxes = document.querySelectorAll('.alert-box')
const chosen_imageBoxes = document.querySelectorAll('.chosen-pic-box')
const save_changes_buttons = document.querySelectorAll('.save-changes-btn')

const choose_profile_pic_btn = document.getElementById('choose-profile-pic-btn')
const frm_change_profile_pic = document.getElementById('frm-change-profile-pic')

const choose_background_pic_btn = document.getElementById('choose-background-pic-btn')
const frm_change_background_pic = document.getElementById('frm-change-background-pic')

const csrf = document.getElementsByName('csrfmiddlewaretoken')

csrf.forEach(function(token) {
    console.log(token.value);
});

choose_profile_pic_btn.addEventListener('change', ()=>{
    alertBoxes.forEach(function(box) {
        box.innerHTML = ""
    })
    save_changes_buttons.forEach(function(btn) {
        btn.disabled = false;
    })
    const img_data = choose_profile_pic_btn.files[0]
    const url = URL.createObjectURL(img_data)
    chosen_imageBoxes.forEach(function(box) {
        box.innerHTML = `<img src="${url}" id="profile-pic-imgfile" width="250px">`
    })
    var $profile_pic = $('#profile-pic-imgfile')
    // aspectRatio: 5/3,
    $profile_pic.cropper({
        aspectRatio: 1/1,
    });
    var cropper = $profile_pic.data('cropper');
    save_changes_buttons.forEach(function(btn) {
        btn.addEventListener('click', ()=>{
            cropper.getCroppedCanvas().toBlob((blob) => {
                const fd = new FormData();
                fd.append('csrfmiddlewaretoken', csrf[0].value)
                fd.append('img', blob, 'profile_img.png');
    
                $.ajax({
                    type:'POST',
                    url: frm_change_profile_pic.action,
                    enctype: 'multipart/form-data',
                    data: fd,
                    success: function(response){
    
                        console.log('success', response)
                        window.location.reload();
                        alertBoxes.forEach(function(box) {
                            box.innerHTML = `<div class="alert alert-success" role="alert">
                                                    Successfully saved and cropped the selected image!
                                                </div>`
                        })
                        
                    },
                    error: function(error){
                        console.log('error', error)
                        alertBoxes.forEach(function(box) {
                            box.innerHTML = `<div class="alert alert-danger" role="alert">
                                                    Something went wrong..
                                                </div>`
                        })
                    },
                    cache: false,
                    contentType: false,
                    processData: false,
                })
            })
        
        })
    })
    
})

choose_background_pic_btn.addEventListener('change', ()=>{
    alertBoxes.forEach(function(box) {
        box.innerHTML = ""
    })
    save_changes_buttons.forEach(function(btn) {
        btn.disabled = false;
    })
    const img_data = choose_background_pic_btn.files[0]
    const url = URL.createObjectURL(img_data)
    chosen_imageBoxes.forEach(function(box) {
        box.innerHTML = `<img src="${url}" id="background-pic-imgfile" width="250px">`
    })
    var $background_pic = $('#background-pic-imgfile')
    $background_pic.cropper({
        aspectRatio: 5/3,
    });
    var cropper = $background_pic.data('cropper');
    save_changes_buttons.forEach(function(btn) {
        btn.addEventListener('click', ()=>{
            cropper.getCroppedCanvas().toBlob((blob) => {
                const fd = new FormData();
                fd.append('csrfmiddlewaretoken', csrf[0].value)
                fd.append('img', blob, 'background_img.png');
    
                $.ajax({
                    type:'POST',
                    url: frm_change_background_pic.action,
                    enctype: 'multipart/form-data',
                    data: fd,
                    success: function(response){
    
                        console.log('success', response)
                        window.location.reload();
                        alertBoxes.forEach(function(box) {
                            box.innerHTML = `<div class="alert alert-success" role="alert">
                                                    Successfully saved and cropped the selected image!
                                                </div>`
                        })
                        
                    },
                    error: function(error){
                        console.log('error', error)
                        alertBoxes.forEach(function(box) {
                            box.innerHTML = `<div class="alert alert-danger" role="alert">
                                                    Something went wrong..
                                                </div>`
                        })
                    },
                    cache: false,
                    contentType: false,
                    processData: false,
                })
            })
        
        })
    })
    
})

