(() => {
    function escapeHtml(value) {
        return String(value ?? '')
            .replaceAll('&', '&amp;')
            .replaceAll('<', '&lt;')
            .replaceAll('>', '&gt;')
            .replaceAll('"', '&quot;')
            .replaceAll("'", '&#39;');
    }

    function getCookie(name) {
        const prefix = `${name}=`;
        const cookie = document.cookie
            .split(';')
            .map((value) => value.trim())
            .find((value) => value.startsWith(prefix));
        return cookie ? decodeURIComponent(cookie.slice(prefix.length)) : null;
    }

    function safeWebUrl(value) {
        const rawValue = String(value ?? '').trim();
        if (!rawValue) return '';

        try {
            const parsedUrl = new URL(rawValue, window.location.origin);
            return ['http:', 'https:'].includes(parsedUrl.protocol)
                ? rawValue
                : '';
        } catch (error) {
            return '';
        }
    }

    window.ajaxUtils = Object.freeze({ escapeHtml, getCookie, safeWebUrl });
})();
