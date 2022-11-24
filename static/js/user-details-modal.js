const userDetailsIcon = document.querySelector('.fa-user');
const userDetailsModal = document.querySelector(".user-details-modal");
const userDetailsModalCloseButton = document.querySelector(".user-details-modal .close-button");
const showChangeDetailsFormButton = document.querySelector(".show-details-form-button");
const showChangePasswordFormButton = document.querySelector(".show-password-form-button");
const changeDetailsForm = document.querySelector(".change-details-form");
const changePasswordForm = document.querySelector(".change-password-form");

window.onclick = function(event) {
    if (event.target === userDetailsModal) {
        userDetailsModal.style.display = "none";
    }
};

userDetailsIcon.addEventListener("click", (e) => {
    e.preventDefault();
    userDetailsModal.style.display = "flex";
});

userDetailsModalCloseButton.addEventListener("click", () => {
    userDetailsModal.style.display = "none"
});

showChangeDetailsFormButton.addEventListener("click", (e) => {
    changePasswordForm.style.display = 'none';
    showChangePasswordFormButton.classList.remove('active');

    changeDetailsForm.style.display = 'flex';
    e.target.classList.toggle('active');
})

showChangePasswordFormButton.addEventListener("click", (e) => {
    changeDetailsForm.style.display = 'none';
    showChangeDetailsFormButton.classList.remove('active');

    changePasswordForm.style.display = 'flex';
    e.target.classList.toggle('active');
})
