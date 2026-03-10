document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('regForm');
    const firstName = document.getElementById('first_name');
    const lastName = document.getElementById('last_name');

    function validateName(input) {
        const nameRegex = /^[A-ZА-ЯЁ][a-zа-яё]+$/;
        
        if (input.value === "") {
            input.setCustomValidity("");
        } else if (!nameRegex.test(input.value)) {
            input.setCustomValidity("Используйте только буквы. Первая должна быть заглавной, остальные — строчными.");
        } else {
            input.setCustomValidity("");
        }
    }

    if (firstName) firstName.addEventListener('input', () => validateName(firstName));
    if (lastName) lastName.addEventListener('input', () => validateName(lastName));

    if (form) {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
                alert("Форма заполнена неверно. Проверьте подсвеченные поля.");
            }
            form.classList.add('was-validated');
        });
    }
});