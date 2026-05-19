document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('regForm');
    const firstName = document.getElementById('first_name');
    const lastName = document.getElementById('last_name');
    const email = document.getElementById('email');
    const age = document.getElementById('age');
    const password = document.getElementById('password');
    const confirm = document.getElementById('confirm_password');

    function showError(input, message) {
        const span = input.nextElementSibling;
        span.textContent = message;
        input.classList.add('border-red-400');
        input.classList.remove('border-amber-200');
    }

    function clearError(input) {
        const span = input.nextElementSibling;
        span.textContent = '';
        input.classList.remove('border-red-400');
        input.classList.add('border-amber-200');
    }

    function validateName(input) {
        const nameRegex = /^[A-ZА-ЯЁ][a-zа-яё]+$/;
        if (input.value === '') {
            clearError(input);
        } else if (!nameRegex.test(input.value)) {
            showError(input, 'Используйте только буквы. Первая должна быть заглавной, остальные — строчными.');
        } else {
            clearError(input);
        }
    }

    function validateEmail(input) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (input.value === '') {
            clearError(input);
        } else if (!emailRegex.test(input.value)) {
            showError(input, 'Введите корректный email.');
        } else {
            clearError(input);
        }
    }

    function validateAge(input) {
        const val = parseInt(input.value);
        if (input.value === '') {
            clearError(input);
        } else if (isNaN(val) || val < 18 || val > 100) {
            showError(input, 'Возраст должен быть от 18 до 100.');
        } else {
            clearError(input);
        }
    }

    function validatePasswords() {
        if (!confirm || !password) return;
        if (!confirm.value.trim()) {
            clearError(confirm);
            return;
        }
        if (password.value !== confirm.value) {
            showError(confirm, 'Пароли не совпадают.');
        } else {
            clearError(confirm);
        }
    }

    function validatePasswordMatchOnSubmit() {
        if (!confirm || !password) return false;
        const p = password.value.trim();
        const c = confirm.value.trim();
        if (p && c && p !== c) {
            showError(confirm, 'Пароли не совпадают.');
            return true;
        }
        return false;
    }

    if (firstName) firstName.addEventListener('input', () => validateName(firstName));
    if (lastName) lastName.addEventListener('input', () => validateName(lastName));
    if (email) email.addEventListener('input', () => validateEmail(email));
    if (age) age.addEventListener('input', () => validateAge(age));
    if (password) password.addEventListener('input', validatePasswords);
    if (confirm) confirm.addEventListener('input', validatePasswords);

    if (form) {
        form.addEventListener('submit', function (event) {
            let hasErrors = false;

            function checkRequired(input, validateFn) {
                if (!input) return;
                if (input.value.trim() === '') {
                    showError(input, 'Поле обязательно для заполнения.');
                    hasErrors = true;
                } else {
                    if (validateFn) validateFn(input);
                    if (input.nextElementSibling.textContent) hasErrors = true;
                }
            }

            checkRequired(firstName, validateName);
            checkRequired(lastName, validateName);
            checkRequired(email, validateEmail);
            checkRequired(age, validateAge);
            checkRequired(password, null);
            checkRequired(confirm, null);
            if (validatePasswordMatchOnSubmit()) {
                hasErrors = true;
            }

            if (hasErrors) {
                event.preventDefault();
            }
        });
    }
});