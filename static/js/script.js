// Toggle Mobile Menu
function toggleMenu() {
    const navLinks = document.getElementById('navLinks');
    // Check current transform property
    if (navLinks.style.transform === 'translateX(0%)') {
      // Close the menu
      navLinks.style.transform = 'translateX(100%)';
    } else {
      // Open the menu
      navLinks.style.transform = 'translateX(0%)';
    }
  }
  