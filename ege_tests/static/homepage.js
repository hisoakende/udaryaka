const get_random_test = () => fetch('http://127.0.0.1:8000/api/get-random-test')
    .then(response =>
        response.json()
    )
    .then(data => {
        create_test(data)
    });


get_random_test();


function create_test(words) {

    function create_answer_options(index) {
        let answer_options = '';
        for (let x = 0; x < words[index].possible_values.length; x++) {
            answer_options += `<label><input type="radio" name="question-${index}"/>
                                    <span>${words[index].possible_values[x]}</span></label>`;
        }
        return answer_options
    }

    const form = document.querySelector('form');
    for (let i = 0; i < 9; i++) {
        form.insertAdjacentHTML('beforeend',
            `<div class="question">${create_answer_options(i)}</div><hr>`);
    }
    form.insertAdjacentHTML('beforeend',
                `<div class="question">${create_answer_options(9)}</div>`)
}
