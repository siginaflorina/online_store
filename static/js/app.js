const navIcons = document.querySelectorAll('nav .icons .icon');

navIcons.forEach(navIcon => {
    navIcon.addEventListener('mouseover', function(){
        navIcon.closest('.icon-container').querySelector('.tooltip').classList.add('active');
    });
    navIcon.addEventListener('mouseout', function(){
        navIcon.closest('.icon-container').querySelector('.tooltip').classList.remove('active');
    });
});
