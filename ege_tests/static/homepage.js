const get_random_test = () => fetch('http://127.0.0.1:8000/api/get-random-test')
    .then(response =>
        response.json()
    )
    .then(data => {
        create_test(data)
    });

get_random_test();

const form = document.querySelector('form');
const row_for_anim = document.querySelector('#row-for-anim');
const btn_start_test = document.querySelector('#start-test');

function create_test(words) {

    function create_answer_options(index) {
        let answer_options = '';
        for (let x = 0; x < words[index].possible_values.length; x++) {
            answer_options += `<label><input type="radio" name="question-${index}"/>
                                    <span>${words[index].possible_values[x]}</span></label>`;
        }
        return answer_options
    }

    for (let i = 0; i < 9; i++) {
        form.insertAdjacentHTML('beforeend',
            `<div class="question">${create_answer_options(i)}</div><hr>`);
    }
    form.insertAdjacentHTML('beforeend',
        `<div class="question">${create_answer_options(9)}</div>`);
}


function start_test() {
    row_for_anim.classList.remove('display-none');
    btn_start_test.parentElement.classList.remove('end-content');
    btn_start_test.innerHTML = 'Пройти другой тест';
    // Анимация прозрачности не проигрывается без setTimeout, и почему так происходит - для меня загадка
    setTimeout(() => {
        row_for_anim.style.opacity = '1'
    }, 1);
}

btn_start_test.addEventListener('click', start_test)
