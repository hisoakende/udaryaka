fetch('http://127.0.0.1:8000/api/get-random-test')
    .then((response) => {return response.json()})
    .then((data) => {create_test(data)});

function create_test(words) {

    function create_answer_options(index) {
        let answer_options = '';
        for (let x = 0; x < words[index].possible_values.length; x++) {
            answer_options +=  `<label><input type="radio" name="question-${index}"/>
                                    <span>${words[index].possible_values[x]}</span></label>`;
        }
        return answer_options
    }

    let task = document.querySelector('.task');
    task.insertAdjacentHTML('afterend', `<div class="question">${create_answer_options(0)}</div>`)
    for (let i = 1; i < 10; i++) {
        task.insertAdjacentHTML('afterend',
            `<div class="question">${create_answer_options(i)}</div><hr>`);
    }
}
