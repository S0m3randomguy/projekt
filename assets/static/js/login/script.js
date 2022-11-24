/* INITIALIZATION */
// Icon definitions

const ICON_SHOW_PASSWORD = "ri-eye-line";
const ICON_HIDE_PASSWORD = "ri-eye-off-line";

// Matching icons to password fields
const MATCH_FIELDS = {
    "password_toggle_login"     : "password_field_login",
    "password_toggle_register"  : "password_field_register",
    "confirmation_toggle"       : "confirmation_field"
}

// Selecting from document
const TOGGLES   = document.querySelectorAll(".showHidePw")

/* SHOW/HIDE PASSWORD */
// Get show/hide icons from ID
// Event handler (password and confirmation)
TOGGLES.forEach(toggle => {
    toggle.addEventListener("click", () => {
        let password_field = document.getElementById(MATCH_FIELDS[toggle.id]);
        if (password_field.type === "password") {
            password_field.type = "text";
            toggle.classList.replace(ICON_HIDE_PASSWORD, ICON_SHOW_PASSWORD)
        } else {
            password_field.type = "password";
            toggle.classList.replace(ICON_SHOW_PASSWORD, ICON_HIDE_PASSWORD)
        }
    })
})