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

// search button activity when zoomed in
// const searchButton = document.getElementById('small-screen-button');
// const originalSearchButton = searchButton.innerHTML;
// let searchButtonIsOriginal = true;

// searchButton.addEventListener('click', function(event) {
//     if (searchButtonIsOriginal) {
//         searchButton.innerHTML = '<i class="fas fa-times" aria-hidden="true"></i>';
//         searchButtonIsOriginal = false;
//     } else {
//         searchButton.innerHTML = originalSearchButton;
//         searchButtonIsOriginal = true;
//     }
// });

// const searchInput = document.querySelector("[data-search]")
  
// searchInput.addEventListener("input", event => {
//     const value = event.target.value
//     console.log(value)
// });

