const toggleButtons = document.querySelectorAll('.toggle-btn');
const visibilityInput = document.getElementById('visibility-input');

toggleButtons.forEach(button => {
    button.addEventListener('click', function() {
        toggleButtons.forEach(btn => btn.classList.remove('active'));
        this.classList.add('active');
        const chosenValue = this.getAttribute('data-value');
        visibilityInput.value = chosenValue;
    });
});

