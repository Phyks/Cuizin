/**
 * Get all locales supported by the client browser.
 */
export function getBrowserLocales() {
    let langs = [];

    if (navigator.languages) {
        // Chrome does not currently set navigator.language correctly
        // https://code.google.com/p/chromium/issues/detail?id=101138
        // but it does set the first element of navigator.languages correctly
        langs = navigator.languages;
    } else if (navigator.userLanguage) {
        // IE only
        langs = [navigator.userLanguage];
    } else {
        // as of this writing the latest version of firefox + safari set this correctly
        langs = [navigator.language];
    }

    // Some browsers does not return uppercase for second part
    const locales = langs.map((lang) => {
        const locale = lang.split('-');
        return locale[1] ? `${locale[0]}-${locale[1].toUpperCase()}` : lang;
    });

    return locales;
}


/**
 * Find the best matching locale from the browser preferred locales.
 *
 * @param messages  A translation object with supported locales as keys.
 * @param defaultLocale An optional default locale.
 * @return The best locale to use.
 */
export function getBestMatchingLocale(messages, defaultLocale = 'en') {
    const locales = getBrowserLocales();

    let bestLocale = defaultLocale;
    // Get best matching locale
    locales.some((locale) => {
        if (messages[locale]) {
            bestLocale = locale;
            // Stop at first matching locale
            return true;
        }
        return false;
    });
    return bestLocale;
}
