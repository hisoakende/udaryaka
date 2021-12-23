const get_random_test = () => fetch('http://127.0.0.1:8000/api/get-random-test')
    .then(response =>
        response.json()
    )
    .then(data => {
        create_test(data)
    });

get_random_test();

const form = document.querySelector('.row-for-anim .col form');
const result = document.querySelector('.result');
const rows_for_anim = document.querySelectorAll('.row-for-anim');
const btn_start_test = document.querySelector('#start-test');
const btn_check_answers = document.querySelector('#check-answers');
let correct_answers = {};
let count_users_answers = new Set();

function create_test(words) {

    function create_answer_options(index) {
        let answer_options = '';
        for (let x = 0; x < words[index].possible_values.length; x++) {
            answer_options += `<label class="question-label"><input type="radio" name="question-${index}" 
                                                            value="${words[index].possible_values[x]}"/>
                                    <span class="question-span">${words[index].possible_values[x]}</span></label>`;
        }
        return answer_options
    }

    const count_of_words = Object.keys(words).length;

    for (let i = 0; i < count_of_words - 1; i++) {
        form.insertAdjacentHTML('beforeend',
            `<div class="question">${create_answer_options(i)}</div><hr>`);
        correct_answers[`question-${i}`] = words[i].possible_values[words[i].correct_value];
    }
    form.insertAdjacentHTML('beforeend',
        `<div class="question">${create_answer_options(count_of_words - 1)}</div>`);
    correct_answers[`question-${count_of_words - 1}`] =
        words[count_of_words - 1].possible_values[words[count_of_words - 1].correct_value];

    document.querySelectorAll('.question label input').forEach(el => {
        el.addEventListener(
            'change', check_change_for_activate_btn)
    })
}


function check_change_for_activate_btn(event) {
    count_users_answers.add(event.target.value.toLowerCase());
    if (count_users_answers.size === Object.keys(correct_answers).length) {
        btn_check_answers.disabled = false
    }
}


function start_test() {
    rows_for_anim.forEach(element => {
        element.classList.remove('display-none')
    });
    btn_start_test.parentElement.classList.remove('end-content');
    btn_start_test.disabled = true;
    // Анимация прозрачности не проигрывается без setTimeout, и почему так происходит - для меня загадка
    setTimeout(() => {
        rows_for_anim.forEach(element => {
            element.style.opacity = '1'
        });
    }, 1);
}

btn_start_test.addEventListener('click', start_test, once = true);


function view_correct(incorrect_answers) {
    document.querySelectorAll('.question label input').forEach(element => {
        element.disabled = true;
        element.parentElement.style.cursor = 'default';
        for (let answer of incorrect_answers) {
            if (answer === element.value) {
                element.parentElement.classList.add('incorrect-answer');
                const correct_answer = correct_answers[`question-${element.name.slice(-1)}`];
                document.querySelector(`input[value=${correct_answer}]`).checked = true;
            }
        }
    })

}


function check_user_answers() {
    const user_answers = new FormData(form);
    const incorrect_answers = [];
    let count_user_correct_answers = 0;
    for (const entry of user_answers) {
        if (correct_answers[entry[0]] === entry[1]) {
            count_user_correct_answers++
        } else {
            incorrect_answers.push(entry[1])
        }
    }
    btn_check_answers.disabled = true;
    btn_check_answers.innerHTML = 'Ответы проверены!';
    btn_start_test.innerHTML = 'Тест пройден!';
    result.innerHTML = `${count_user_correct_answers}/${Object.keys(correct_answers).length}`;
    document.querySelectorAll('.question-span').forEach(label => {
        label.removeEventListener(
            'change', check_change_for_activate_btn)
    })
    view_correct(incorrect_answers);
}

btn_check_answers.addEventListener('click', check_user_answers, once = true);
