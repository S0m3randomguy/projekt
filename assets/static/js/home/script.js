/* INITIALIZATION */
// Icon definitions
const ICON_OPEN_DROPDOWN = "ri-arrow-up-s-line";
const ICON_CLOSED_DROPDOWN = "ri-arrow-down-s-line";

// Selecting from document
const DROPDOWN_BUTTON = document.querySelector(".drop-btn");
const DROPDOWN_CONTENT = document.querySelector(".dropdown-content");
const ARROW = document.querySelector(".arrow");
const HAMBURGER = document.querySelector('.hamburger');
const HAMBURGER_ICON = HAMBURGER.querySelector('span');
const MOBILE_MENU = document.querySelector('.mobile-menu');
const SEARCH_BUTTON = document.querySelector('.tablet-search');
const INPUT_BOX = document.querySelector('.input-box');
const INPUT = document.querySelector('input');
const NAVBAR_ITEMS = document.querySelector('.navbar-items');
const MOBILE_DROPDOWN_BUTTON = document.querySelector('.mobile-menu ul li .drop-btn');
const MOBILE_DROPDOWN_CONTENT = document.querySelector('.mobile-menu .mobile-dropdown-content');
const MOBILE_ARROW = document.querySelector('.mobile-menu ul li .arrow');
const MOBILE_SEARCH_BAR = document.querySelector('.mobile-input-box');
const MOBILE_INPUT = document.querySelector('.mobile-input-box input');
const MOBILE_SEARCH_BUTTON = document.querySelector('.mobile-search-button');


/* SHOW/HIDE DROPDOWN CONTENT */
// Toggle dropdown class on button click
// Change arrow direction
DROPDOWN_BUTTON.addEventListener("click", () => {
  DROPDOWN_CONTENT.classList.toggle("show");
  if (ARROW.classList == (ICON_CLOSED_DROPDOWN + " arrow")) {
    ARROW.classList.replace(ICON_CLOSED_DROPDOWN, ICON_OPEN_DROPDOWN);
  }
  else {
    ARROW.classList.replace(ICON_OPEN_DROPDOWN, ICON_CLOSED_DROPDOWN);
  }
})

// Remove "show" from dropdown content class and change arrow direction if user clicks outside of the dropdown button
window.addEventListener("click", (event) => {
  if (!event.target.matches('.drop-btn')) {
      if (DROPDOWN_CONTENT.classList.contains('show')) {
        DROPDOWN_CONTENT.classList.remove('show');
        if (ARROW.classList == (ICON_CLOSED_DROPDOWN + " arrow")) {
          ARROW.classList.replace(ICON_CLOSED_DROPDOWN, ICON_OPEN_DROPDOWN);
        }
        else {
          ARROW.classList.replace(ICON_OPEN_DROPDOWN, ICON_CLOSED_DROPDOWN);
        }
      }
    }
  }
)

/* TABLET MENU */
/* SHOW/HIDE SEARCH BAR ON "SEARCH" NAVBAR ITEM CLICK */
// Open, focus on search bar
SEARCH_BUTTON.addEventListener('click', () => {
	INPUT_BOX.style.display = "block";
  NAVBAR_ITEMS.style.display = "none";
  INPUT.focus();
})

// Hide search bar if it's not focused
// If the window width is greater than 1000px, hide tablet menu.
setInterval(checkWidth, 1)
function checkWidth() {
  if (window.innerWidth < 1001) {
      if (document.activeElement === INPUT) {
        INPUT_BOX.style.display = "block";
        NAVBAR_ITEMS.style.display = "none";
      }
      else {
        INPUT_BOX.style.display = "none";
        NAVBAR_ITEMS.style.display = "flex";
      }
  }
  else {
    INPUT_BOX.style.display = "block";
    NAVBAR_ITEMS.style.display = "flex";
  }
}

/* MOBILE MENU */
/* CHANGE HAMBURGER ICON AND OPEN MOBILE MENU */
HAMBURGER.addEventListener('click', () => {
	HAMBURGER.classList.toggle("x");
	MOBILE_MENU.classList.toggle('open');
  MOBILE_MENU.style.transition = "all 0.3s";
  if (MOBILE_DROPDOWN_CONTENT.classList.contains("show")) {
    MOBILE_DROPDOWN_CONTENT.classList.remove("show");
    // (TO DO: make a short pause here before also closing the mobile menu)
    MOBILE_MENU.classList.remove("up");
  }
})

/* OPEN DROPDOWN MENU */
MOBILE_DROPDOWN_BUTTON.addEventListener("click", () => {
  MOBILE_MENU.style.transition = "all 0s";
  MOBILE_DROPDOWN_CONTENT.classList.toggle("show");
  MOBILE_MENU.classList.toggle("up");
  if (MOBILE_ARROW.classList == (ICON_CLOSED_DROPDOWN + " arrow")) {
    MOBILE_ARROW.classList.replace(ICON_CLOSED_DROPDOWN, ICON_OPEN_DROPDOWN);
  }
  else {
    MOBILE_ARROW.classList.replace(ICON_OPEN_DROPDOWN, ICON_CLOSED_DROPDOWN);
  }
})

/* OPEN SEARCH BAR ON BUTTON CLICK */
MOBILE_SEARCH_BUTTON.addEventListener("click", () => {
  MOBILE_MENU.style.transition = "all 0s";
  MOBILE_SEARCH_BAR.classList.toggle("show");
  MOBILE_SEARCH_BUTTON.classList.toggle("hide");
  MOBILE_MENU.classList.toggle("search-up");
  MOBILE_INPUT.focus();
})

// Hide mobile search bar if it's not focused
setInterval(mobileWidth, 1)
function mobileWidth() {
  if (window.innerWidth < 570) {
    if (MOBILE_SEARCH_BAR.classList.contains("show")) {
      if (document.activeElement === MOBILE_INPUT) {

      }
      else {
        MOBILE_SEARCH_BAR.classList.toggle("show");
        MOBILE_SEARCH_BUTTON.classList.toggle("hide");
        MOBILE_MENU.classList.toggle("search-up");
      }
    }
  }
}
