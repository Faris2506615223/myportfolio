(() => {
    const toggle = document.querySelector('.site-nav-toggle');
    const navigation = document.querySelector('.site-navigation');

    if (!toggle || !navigation) return;

    const setOpen = (isOpen) => {
        toggle.classList.toggle('active', isOpen);
        navigation.classList.toggle('active', isOpen);
        toggle.setAttribute('aria-expanded', String(isOpen));
        toggle.setAttribute('aria-label', isOpen ? 'Tutup navigasi' : 'Buka navigasi');
    };

    toggle.addEventListener('click', () => {
        setOpen(toggle.getAttribute('aria-expanded') !== 'true');
    });

    navigation.querySelectorAll('a').forEach((link) => {
        link.addEventListener('click', () => setOpen(false));
    });

    document.addEventListener('keydown', (event) => {
        if (event.key === 'Escape') setOpen(false);
    });

    window.addEventListener('resize', () => {
        if (window.innerWidth > 760) setOpen(false);
    }, { passive: true });
})();
