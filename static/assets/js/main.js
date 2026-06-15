document.addEventListener('DOMContentLoaded', function () {

    initSwipers();

    function initSwipers(selector = "[data-swiper]") {
        document.querySelectorAll(selector).forEach((el) => {
            const options = el.dataset.swiper ? JSON.parse(el.dataset.swiper) : {};
            el.swiperInstance = new Swiper(el, options);
        });

        // کنترل thumbnail برای هر اسلایدر
        document.querySelectorAll('.thumbnail').forEach(thumb => {
            thumb.addEventListener('click', () => {
                const index = Number(thumb.dataset.index);

                // نزدیک‌ترین اسلایدر والد را پیدا کن
                const swiperEl = thumb.closest('.swiper');

                if (swiperEl?.swiperInstance) {
                    // اگر loop فعال است:
                    swiperEl.swiperInstance.slideToLoop(index, 800);
                }
            });
        });
    }
});