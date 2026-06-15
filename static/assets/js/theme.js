// Theme toggle - runs immediately to prevent FOUC (Flash of Unstyled Content)
(function () {
    const saved = localStorage.getItem('theme');
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;

    if (saved === 'light') {
        document.documentElement.classList.remove('dark');
    } else if (saved === 'dark') {
        document.documentElement.classList.add('dark');
    } else {
        // No saved preference: default to dark (original design)
        if (prefersDark || !saved) {
            document.documentElement.classList.add('dark');
        }
    }
})();

// Toggle between light and dark mode
function toggleTheme() {
    const html = document.documentElement;
    const isDark = html.classList.toggle('dark');
    localStorage.setItem('theme', isDark ? 'dark' : 'light');
}