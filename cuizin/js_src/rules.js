export const url = [
    (v) => {
        if (!v) {
            return true;
        }
        try {
            new URL(v);  // eslint-disable-line no-new
            return true;
        } catch (e) {
            return this.$t('new.url_must_be_valid');
        }
    },
];
