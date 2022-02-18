document.querySelector('.a-authenticated-important').addEventListener('click', () => {
    fetch(`http://${document.location.host}/manage-user/api/send-mail-for-activation`).then(response => {
        window.location.href = `http://${document.location.host}/manage-user/key-verification`;
    })
});
