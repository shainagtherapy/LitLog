// Modals



const loginModal = document.getElementById("login-modal")
const loginButton = document.getElementById("login-button")

loginButton.addEventListener("click", () => {
    loginModal.showModal();
})