//
// Layout
//

'use strict';

const currentLocation = location.href;

const menuItem = document.querySelectorAll('.nav-link');

menuItem.forEach(item => {
    if (item.href===currentLocation) {
        item.classList.toggle('active');
    }
});
