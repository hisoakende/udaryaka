function check_test_for_existence(e) {
    e.preventDefault();
    const form = new FormData(document.querySelector('.right-content form'));
    const test_id = form.get('test-id')
    fetch(`http://127.0.0.1:8000/api/check_test_for_existence/${test_id}`).then(response => {
        switch (response.status) {
            case 200:
                window.location.href = `http://127.0.0.1:8000/tests/id=${test_id}`
                break
            case 204:
                break
        }
    })
}


document.querySelector('#find-test').addEventListener('click', check_test_for_existence);
