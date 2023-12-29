

const bg_alertBox = document.getElementById('bg-alert-box')
const chosen_background_img_box = document.getElementById('chosen-background-img-box')
const bg_save_changes_btn = document.getElementById('bg-save-changes-btn')
const frm_change_background_pic = document.getElementById('frm-change-background-pic')
const choose_background_pic_btn = document.getElementById('choose-background-pic-btn')

const csrf = document.getElementsByName('csrfmiddlewaretoken')

choose_background_pic_btn.addEventListener('change', ()=>{
    bg_alertBox.innerHTML = ""
    bg_save_changes_btn.disabled = false;
    const img_data = choose_background_pic_btn.files[0]
    const url = URL.createObjectURL(img_data)
    chosen_background_img_box.innerHTML = `<img src="${url}" id="profile-pic-imgfile" width="250px">`        
    var $profile_pic = $('#profile-pic-imgfile')
    $profile_pic.cropper({
        aspectRatio: 5/3,
    });
    var cropper = $profile_pic.data('cropper');
    bg_save_changes_btn.addEventListener('click', ()=>{
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
                    bg_alertBox.innerHTML = `<div class="alert alert-success" role="alert">
                                            Successfully saved and cropped the selected image!
                                        </div>`
                    
                },
                error: function(error){
                    console.log('error', error)
                    bg_alertBox.innerHTML = `<div class="alert alert-danger" role="alert">
                                            Something went wrong..
                                        </div>`
                },
                cache: false,
                contentType: false,
                processData: false,
            })
        })
    
    })
    
})







const pf_alertBox = document.getElementById('pf-alert-box');
const chosen_profile_img_box = document.getElementById('chosen-profile-img-box');
const pf_save_changes_btn = document.getElementById('pf-save-changes-btn');
const frm_change_profile_pic = document.getElementById('frm-change-profile-pic');
const choose_profile_pic_btn = document.getElementById('choose-profile-pic-btn');

choose_profile_pic_btn.addEventListener('change', () => {
    pf_alertBox.innerHTML = '';
    pf_save_changes_btn.disabled = false;

    const img_data = choose_profile_pic_btn.files[0];
    const url = URL.createObjectURL(img_data);
    chosen_profile_img_box.innerHTML = `<img src="${url}" id="profile-pic-imgfile" width="250px">`;

    var $profile_pic = $('#profile-pic-imgfile');
    $profile_pic.cropper({
        aspectRatio: 1 / 1,
    });

    var cropper = $profile_pic.data('cropper');

    pf_save_changes_btn.addEventListener('click', () => {
        cropper.getCroppedCanvas().toBlob((blob) => {
            const fd = new FormData();
            fd.append('csrfmiddlewaretoken', csrf[0].value);
            fd.append('img', blob, 'profile_img.png');

            $.ajax({
                type: 'POST',
                url: frm_change_profile_pic.action,
                enctype: 'multipart/form-data',
                data: fd,
                success: function (response) {
                    console.log('success', response);
                    window.location.reload();
                    pf_alertBox.innerHTML = `<div class="alert alert-success" role="alert">
                                                Successfully saved and cropped the selected image!
                                            </div>`;
                },
                error: function (error) {
                    console.log('error', error);
                    pf_alertBox.innerHTML = `<div class="alert alert-danger" role="alert">
                                                Something went wrong..
                                            </div>`;
                },
                cache: false,
                contentType: false,
                processData: false,
            });
        });
    });
});
