// Modals



const loginModal = document.getElementById("login-modal")
const loginButton = document.getElementById("login-button")

loginButton.addEventListener("click", () => {
    loginModal.showModal();
})



const signupModal = document.getElementById("signup-modal")
const signupButton = document.getElementById("signup-button")

signupButton.addEventListener("click", () => {
    signupModal.showModal();
})