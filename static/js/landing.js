(() => {
    const body = document.body;
    const entrance = document.querySelector('#entrance-gate');
    const enterButton = document.querySelector('#enter-btn');
    const progress = document.querySelector('#scroll-progress');
    const header = document.querySelector('#navbar');
    const backToTop = document.querySelector('#back-to-top');
    const parallaxImage = document.querySelector('.hero-parallax-img');
    const mobileToggle = document.querySelector('#mobile-toggle');
    const navLinks = document.querySelector('#nav-links');
    const navItems = [...document.querySelectorAll('.nav-item')];
    const sections = [...document.querySelectorAll('#about')];

    if (entrance) {
        body.classList.add('entrance-open');
        enterButton?.focus({ preventScroll: true });
        enterButton?.addEventListener('click', () => {
            entrance.classList.add('is-leaving');
            body.classList.remove('entrance-open');
            window.setTimeout(() => entrance.remove(), 900);
        });
    }

    mobileToggle?.addEventListener('click', () => {
        const isOpen = mobileToggle.classList.toggle('active');
        navLinks?.classList.toggle('active', isOpen);
        mobileToggle.setAttribute('aria-expanded', String(isOpen));
        mobileToggle.setAttribute('aria-label', isOpen ? 'Close menu' : 'Open menu');
    });

    navItems.forEach((item) => {
        item.addEventListener('click', () => {
            mobileToggle?.classList.remove('active');
            navLinks?.classList.remove('active');
            mobileToggle?.setAttribute('aria-expanded', 'false');
        });
    });

    const revealObserver = new IntersectionObserver((entries) => {
        entries.forEach((entry) => {
            if (entry.isIntersecting) {
                entry.target.classList.add('is-visible');
                revealObserver.unobserve(entry.target);
            }
        });
    }, { threshold: .13, rootMargin: '0px 0px -30px' });

    document.querySelectorAll('.fade-up-el').forEach((element) => revealObserver.observe(element));

    let previousScroll = window.scrollY;
    let ticking = false;

    const updateOnScroll = () => {
        const currentScroll = window.scrollY;
        const scrollable = document.documentElement.scrollHeight - window.innerHeight;
        const percentage = scrollable > 0 ? (currentScroll / scrollable) * 100 : 0;

        if (progress) progress.style.width = `${Math.min(100, percentage)}%`;
        if (header) {
            header.classList.toggle('scroll-down', currentScroll > previousScroll && currentScroll > 180);
        }
        backToTop?.classList.toggle('visible', currentScroll > window.innerHeight * .7);

        if (parallaxImage && currentScroll < window.innerHeight * 1.2) {
            parallaxImage.style.transform = `translate3d(0, ${currentScroll * .12}px, 0)`;
        }

        const marker = currentScroll + window.innerHeight * .38;
        let activeId = '';
        sections.forEach((section) => {
            if (marker >= section.offsetTop) activeId = section.id;
        });
        navItems.forEach((item) => {
            item.classList.toggle('active', item.getAttribute('href') === `#${activeId}`);
        });

        previousScroll = Math.max(0, currentScroll);
        ticking = false;
    };

    window.addEventListener('scroll', () => {
        if (!ticking) {
            window.requestAnimationFrame(updateOnScroll);
            ticking = true;
        }
    }, { passive: true });

    backToTop?.addEventListener('click', () => window.scrollTo({ top: 0, behavior: 'smooth' }));
    updateOnScroll();

    if (window.matchMedia('(pointer: fine)').matches) {
        const dot = document.querySelector('.cursor-dot');
        const ring = document.querySelector('.cursor-ring');
        let pointerX = -100;
        let pointerY = -100;
        let ringX = -100;
        let ringY = -100;

        window.addEventListener('mousemove', (event) => {
            pointerX = event.clientX;
            pointerY = event.clientY;
            if (dot) dot.style.transform = `translate3d(${pointerX}px, ${pointerY}px, 0) translate(-50%, -50%)`;
        }, { passive: true });

        const animateCursor = () => {
            ringX += (pointerX - ringX) * .16;
            ringY += (pointerY - ringY) * .16;
            if (ring) ring.style.transform = `translate3d(${ringX}px, ${ringY}px, 0) translate(-50%, -50%)`;
            window.requestAnimationFrame(animateCursor);
        };
        animateCursor();

        document.querySelectorAll('a, button, .tech-card, .project-item').forEach((element) => {
            element.addEventListener('mouseenter', () => ring?.classList.add('hover-active'));
            element.addEventListener('mouseleave', () => ring?.classList.remove('hover-active'));
        });
    }
})();
