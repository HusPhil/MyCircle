const csrf = document.getElementsByName('csrfmiddlewaretoken')

//IMAGE CROPPER for Changing Circle Picture
function imageCropper(
    selectedImgBox, saveChangesBtn, fileInput, 
    receiverForm, picContainer, 
    frmSubmitBtn, inputRoomID, inputCircleName) {
    fileInput.addEventListener('change', () => {
        saveChangesBtn.disabled = false;
    
        const img_data = fileInput.files[fileInput.files.length - 1];
        const url = URL.createObjectURL(img_data);
        selectedImgBox.innerHTML = `<img src="${url}" id="profile-pic-imgfile" width="250px">`;
    
        var $profile_pic = $('#profile-pic-imgfile');
        $profile_pic.cropper({
            aspectRatio: 1 / 1,
        });
    
        var cropper = $profile_pic.data('cropper');
    
        saveChangesBtn.addEventListener('click', () => {
            cropper.getCroppedCanvas().toBlob((blob) => {                
                const fd = new FormData();
                fd.append('csrfmiddlewaretoken', csrf[0].value);
                fd.append('circle_img', blob, 'circle_picture.png');
                fd.append(inputRoomID.name, inputRoomID.value);
                fd.append(inputCircleName.name, inputCircleName.value);
                // imgDataCont.value = fd.get('img')

                const blobUrl = URL.createObjectURL(blob);
                picContainer.src = blobUrl

                frmSubmitBtn.addEventListener('click', (e) => {
                    console.log('submitted')
                    $.ajax({
                        type:'POST',
                        url: receiverForm.action,
                        enctype: 'multipart/form-data',
                        data: fd,
                        success: window.location.reload(),
                        cache: false,
                        contentType: false,
                        processData: false,
                    })
                })
                
            });
        });
    });
}



//create circle form validation
var checkBoxes = document.querySelectorAll(`input[type="checkbox"][name="${createCircleFrmName}"]`);

function getCheckedBoxes(parent) {
    const parentElement = document.getElementById(parent)
    if(parentElement){
        return parentElement.querySelectorAll(`input[type="checkbox"][name="${createCircleFrmName}"]:checked`)
    }
}

checkBoxes.forEach((checkBox) => {
    checkBox.addEventListener('click', (e) => {
        const parentFrmId = 'create-circle-frm-frn'
        const checkedBoxes = getCheckedBoxes(parentFrmId)
        const createFrnCircleBtn = document.getElementById('new-circle-msg-btn')

        if(checkedBoxes && checkedBoxes.length == 1) {
            createFrnCircleBtn.disabled = false
            checkBoxes.forEach((checkBox) => {
                checkBox.disabled = true
            })
            checkedBoxes[0].disabled = false
        }
        else if(checkedBoxes.length == 0) {
            checkBoxes.forEach((checkBox) => {
                checkBox.disabled = false
            })
        }
        else {
            createFrnCircleBtn.disabled = true
            var errorMessage = 
            '<p style="color: rgb(177, 46, 46);">Please select only one friend.</p>'
            
            const errorMessageCont = $('#create-circle-frn-error').empty();
            errorMessageCont.append(errorMessage)
        }
    })
})



if(document.getElementById('create-circle-frm-stn')) {
    document.getElementById('create-circle-frm-stn').addEventListener('submit', function(event) {
        if (getCheckedBoxes('create-circle-frm-stn').length < 2) {
            event.preventDefault(); 
            var errorMessage = 
            '<p style="color: rgb(177, 46, 46);">Please select atleast 2 members.</p>'
            
            const errorMessageCont = $('#create-circle-stn-error').empty();
            errorMessageCont.append(errorMessage)
        }
    });
}


// Function to check the message input and perform related actions
function checkMsgInput() {
    showMsgSendBtn();
    autoResize();
}

// Function to show or hide the send message button based on the message input
function showMsgSendBtn() {
    const messageInput = document.getElementById('message-input').value.trim();
    const sendMsgBtn = document.getElementById('send-message-btn');
    sendMsgBtn.disabled = messageInput === '';
}

// Function to automatically resize the textarea height
function autoResize() {
    const textarea = document.getElementById('message-input');
    textarea.style.height = 'auto';
    textarea.style.height = `${textarea.scrollHeight}px`;
}

// Function to scroll to the bottom of the scrolling container
let previousMessageCount = 0;
function scrollToBottom() {
    const chatMessages = document.getElementById('chat-messages');
    const isNewMessageArrived = chatMessages.children.length > previousMessageCount;

    if (isNewMessageArrived) {
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    previousMessageCount = chatMessages.children.length;


}

// Function to handle message appending
function messageAppended(messages) {
    const parsedMessages = JSON.parse(messages);
    const chatMessages = $('#chat-messages').empty();
    const today = new Date();

    parsedMessages.forEach(function (message) {
        var formattedContent = message.content.replace(/\n/g, '<br>');

                var formattedContent = message.content.replace(/\n/g, '<br>');

                const dateString = message.timestamp;
                const date = new Date(dateString);
                const today = new Date();

                if (
                  date.getDate() === today.getDate() &&
                  date.getMonth() === today.getMonth() &&
                  date.getFullYear() === today.getFullYear()
                ) {
                  const hours = date.getHours();
                  const amPM = hours >= 12 ? 'PM' : 'AM';
                  const formattedHours = hours % 12 || 12;

                  const formattedTime = `Today at ${String(formattedHours).padStart(2, '0')}:${String(date.getMinutes()).padStart(2, '0')} ${amPM}`;
                  var formattedDateTime = formattedTime + ' UTC';
                } else {
                  const hours = date.getHours();
                  const amPM = hours >= 12 ? 'PM' : 'AM';
                  const formattedHours = hours % 12 || 12;

                  formattedDateTime = `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}-${String(date.getDate()).padStart(2, '0')} at ${String(formattedHours).padStart(2, '0')}:${String(date.getMinutes()).padStart(2, '0')} ${amPM} UTC`;
                }        
        const messageBodyClass = current_user === message.sender ? 'message-sent' : 'message-received';
        const senderPicClass = current_user === message.sender ? 'display-hidden' : '';

        const messageBody =
            `<div class="message-item ${messageBodyClass}">
                <img src="${message.sender_pic_url}" alt="sender-pic" class="profile-pic-icon ${senderPicClass}">
                <div class="message-body">
                    <p class="sender-info">@${message.sender}</p>
                    <p class="message-content">${formattedContent}</p>
                </div>
            </div>`;

        chatMessages.append(messageBody);
    });
}

// Function to fetch messages
function fetchMessages() {
    const chatroomId = $('#room_id').val();

    if(currentUrl == 'view_convo') {
        $.ajax({
            url: 'get_messages/' + chatroomId,
            method: 'GET',
            success: function (response) {
                messageAppended(response.messages);
                scrollToBottom();
            },
            error: function (xhr, status, error) {
                console.error('Error fetching messages:', error);
            }
        });
    }
}

// Document ready
$(document).ready(function () {
    $('#message-form').submit(function (event) {
        event.preventDefault();
        const message = $('#message-input').val();

        $.ajax({
            type: 'POST',
            url: 'send_message',
            data: {
                message: message,
                room_id: $('#room_id').val(),
                'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val()
            },
            success: function (response) {
                console.log('Message sent successfully');
                $('#message-input').val('');
            },
            error: function (error) {
                console.error('Error sending message:', error);
            }
        });
    });

    $('#send-message-btn').on('click', function () {
        fetchMessages();
        
    });
    if(currentUrl == 'view_convo') {
        setInterval(fetchMessages, 1000);
    }
});

//Search users by username
const searchByAtrrInputs = document.querySelectorAll('.search-by-attr')

fetch(getFriendsAsJsonUrl)
    .then(res => res.json())
    .then(data => {
        var friends_data = JSON.parse(data.friends)
        displayFriendsList(friends_data)
    })
    .catch(error => console.error('Error:', error));

function displayFriendsList(friends) {
    friends.forEach((friend) => {
        
    })
}

searchByAtrrInputs.forEach((searchInput) => {
    searchInput.addEventListener('keyup', (e) => {
        let searchValue = e.target.value
        const profileListItems = document.querySelectorAll('.profile-option-item')
        profileListItems.forEach((profile) => {
            const p_child = profile.querySelector('p')
            
            profile.style.display = 'none'
           
            if(p_child.getAttribute('test-name').toLowerCase().includes(searchValue.toLowerCase())){
                profile.style.display = 'flex'
            }
            
        })
        

    })
}) 

//change current circle pic
const currentCirclePicCont = document.getElementById('current-circle-pic')
const circleSettingsFrm = document.getElementById('circle-settings-frm')
const submitBtn = document.getElementById('save-circle-settings')

// function changeCurrentCirclePic(new_src) {
//     currentCirclePicCont.src = new_src
//     // console.log(currentCirclePicCont)
// }

// chooseNewCirclePicInputTypeFile.addEventListener('click', (e) => {
//     e.preventDefault()
    
//     changeCurrentCirclePic(e.target.files[0])

//     const reader = new FileReader();

    
//     reader.onload = function () {
//         currentCirclePicCont.src = reader.result
//     };

//     reader.readAsDataURL(e.target.files[0])
//     console.log(reader.readAsDataURL(e.target.files[0]))
// })

const chosenCirclePicBox = document.getElementById('chosen-circle-img-box');
const circlePicChangeSaveBtn = document.getElementById('circle-pic-save-changes-btn');
const circlePicInputFile = document.getElementById('choose-circle-pic-btn');
const circleChRoomId = document.getElementById('circle-room-id')
const circleName = document.getElementById('setting-circle-name')

imageCropper(
    chosenCirclePicBox, circlePicChangeSaveBtn, 
    circlePicInputFile, circleSettingsFrm, 
    currentCirclePicCont, submitBtn, 
    circleChRoomId, circleName)







// function previewImage(event) {
//     const imagePreview = document.getElementById('imagePreview');
//     const create_post_btn = document.getElementById('create_post_btn');
//     imagePreview.style.display = "block"
//     const file = event.target.files[0];
//     const reader = new FileReader();

//     reader.onload = function () {
//         imagePreview.src = reader.result;
//     };

//     if (file) {
//         reader.readAsDataURL(file);
//         create_post_btn.disabled = false;
//     }
// }


