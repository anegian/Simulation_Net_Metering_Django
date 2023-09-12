// variables initialization
const timestamp = new Date().getTime();
const mainContent = document.getElementById("main-index-content-for-all");
const menuNavbar = document.getElementById("nav-list");
// const searchBox = document.getElementById("search-box")
const sideNavbarButton = document.getElementById("menu-nav-button");
let originalButton = sideNavbarButton.innerHTML;
let sideNavbarButtonIsOriginal = true;

// Store the element's initial position
const initialPositionMenu = {top: '100px', left: '-240px' };
const afterClickPositionMenu = {top: '100px', left: '0px' };

// Reset the elements' position to the initial position
menuNavbar.style.top = initialPositionMenu.top;
menuNavbar.style.left = initialPositionMenu.left;



// when the menu navigation button is clicked, the side navbar is shown and the main content becomes blur
sideNavbarButton.addEventListener('click', function(event) {
    
        if (sideNavbarButtonIsOriginal) {
            sideNavbarButton.innerHTML = '<i class="fas fa-times" aria-hidden="true"></i>';
            sideNavbarButtonIsOriginal = false;
            mainContent.classList.add('blurred');
            menuNavbar.style.top = afterClickPositionMenu.top;
            menuNavbar.style.left = afterClickPositionMenu.left;

            // add resize event listener to window
            window.addEventListener('resize', function(event) {
            
                mainContent.classList.remove('blurred');
            });

        } else {
            sideNavbarButton.innerHTML = originalButton;
            sideNavbarButtonIsOriginal = true;
            mainContent.classList.remove('blurred');
            // Reset the elements' position to the initial position
            menuNavbar.style.top = initialPositionMenu.top;
            menuNavbar.style.left = initialPositionMenu.left;

        }
});

// Get the elements by their IDs
const profitText = document.getElementById('profitText');
const profitPercentValue = document.getElementById('profitPercentValue');
const tickOrDash = document.getElementById('tickOrDash');

// Set the value of profitPercent and text color
profitPercentValue.textContent = profitPercent + '%';

if (profitPercent === 100) {
  profitText.style.color = '#738725';
  tickOrDash.textContent = '✔'; // Green tick
} else {
  profitText.style.color = 'lightgrey';
  tickOrDash.textContent = '-'; // Grey dash
}