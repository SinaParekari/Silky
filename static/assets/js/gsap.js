gsap.registerPlugin(ScrollTrigger, ScrollToPlugin);

const lenis = new Lenis({
    duration: 2.5,
    easing: (t) => Math.min(1, 1.001 - Math.pow(2, -10 * t)),
    smoothWheel: true,

});

lenis.on('scroll', ScrollTrigger.update);

gsap.ticker.add((time) => {
    lenis.raf(time * 1000);
});

gsap.ticker.lagSmoothing(0);

document.addEventListener('click', (e) => {
    const anchor = e.target.closest('a[href^="#"]');
    if (!anchor) return;

    const targetId = anchor.getAttribute('href');
    if (!targetId || targetId === '#') return;

    const targetEl = document.querySelector(targetId);
    if (!targetEl) return;

    e.preventDefault();

    const offset = 0;
    lenis.scrollTo(targetEl, { offset: offset });
});


document.querySelectorAll('.fadeIn-top-to-botton').forEach(el => {
    const staggerTime = parseFloat(el.getAttribute('data-stagger')) || 0;

    gsap.from(el, {
        opacity: 0,
        y: -50,
        duration: 1,
        ease: "power2.out",
        delay: staggerTime,
        scrollTrigger: {
            trigger: el,
            start: "top 85%",
            toggleActions: "play none none none",
            markers: false
        }
    });
});


document.querySelectorAll('.fadeIn-botton-to-top').forEach(el => {
    const staggerTime = parseFloat(el.getAttribute('data-stagger')) || 0;

    gsap.from(el, {
        opacity: 0,
        y: 150,
        duration: 3,
        ease: "power2.out",
        delay: staggerTime,
        scrollTrigger: {
            trigger: el,
            start: "top 55%",
            toggleActions: "play none none none",
            markers: false
        }
    });
});