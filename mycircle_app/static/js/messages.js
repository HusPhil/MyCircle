//create circle form validation

document.getElementById('create-circle-frm').addEventListener('submit', function(event) {
    const checkboxes = document.querySelectorAll(`input[type="checkbox"][name="${createCircleFrmName}"]:checked`);
    if (checkboxes.length < 2) {
        event.preventDefault(); 
        var errorMessage = 
        '<p style="color: rgb(177, 46, 46);">Please select atleast 2 members.</p>'
        
        const errorMessageCont = $('#create-circle-error').empty();
        console.log(errorMessageCont)

        errorMessageCont.append(errorMessage)
    }
});



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
                <img src="${message.sender_pic_url}" alt="sender-pic" class="sender-pic ${senderPicClass}">
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



