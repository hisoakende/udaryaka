const timer = document.querySelector('.redirect-timer');
let remaining_time = 4;


function main() {
    setTimeout(() => {
        timer.innerHTML = String(remaining_time);
        remaining_time--;
        if (remaining_time !== -1) {
            main();
        } else {
            window.location.href = `http://${document.location.host}/`
        }
    }, 1000)
}

main();