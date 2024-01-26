document.addEventListener('DOMContentLoaded', function() {
    const togglePasswordBtn = document.querySelector('.toggle-password');
    const passwordField = document.querySelector('#id_password');
    const confirmPasswordField = document.querySelector('#id_confirm_password');
    
    togglePasswordBtn.addEventListener('click', function() {
        const type = passwordField.getAttribute('type') === 'password' ? 'text' : 'password';
        passwordField.setAttribute('type', type);
        confirmPasswordField.setAttribute('type', type);
        this.innerHTML = type === 'password' ? '<i class="fas fa-eye" aria-hidden="true"></i>' : '<i class="fas fa-eye-slash" aria-hidden="true"></i>';
    });
});