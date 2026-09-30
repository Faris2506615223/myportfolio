(() => {
    const app = document.getElementById('experience-app');
    if (!app) return;

    const { getCookie, safeWebUrl } = window.ajaxUtils;
    const SEARCH_DEBOUNCE_DELAY = 300;
    const UUID_PLACEHOLDER = '00000000-0000-0000-0000-000000000000';
    const IS_AUTHENTICATED = app.dataset.isAuthenticated === 'true';
    const CAN_EDIT = app.dataset.canEdit === 'true';
    const CAN_DELETE = app.dataset.canDelete === 'true';

    const loadingState = document.getElementById('experience-loading');
    const errorState = document.getElementById('experience-error');
    const emptyState = document.getElementById('experience-empty');
    const gridContainer = document.getElementById('experience-grid');
    const searchForm = document.getElementById('experience-search-form');
    const searchInput = document.getElementById('experience-search-input');
    const experienceForm = document.getElementById('experience-form');
    let requestController;
    let searchTimer;

    function setVisibleState({ loading = false, error = false, empty = false, grid = false }) {
        loadingState.classList.toggle('hide', !loading);
        errorState.classList.toggle('hide', !error);
        emptyState.classList.toggle('hide', !empty);
        gridContainer.classList.toggle('hide', !grid);
    }

    function endpointFromTemplate(template, id) {
        return template.replace(UUID_PLACEHOLDER, encodeURIComponent(id));
    }

    function createElement(tagName, className, text) {
        const element = document.createElement(tagName);
        if (className) element.className = className;
        if (text !== undefined) element.textContent = String(text);
        return element;
    }

    function createCsrfInput() {
        const input = document.createElement('input');
        input.type = 'hidden';
        input.name = 'csrfmiddlewaretoken';
        input.value = getCookie('csrftoken') || '';
        return input;
    }

    function buildStarForm(experience, experienceId) {
        const form = createElement('form', 'star-form');
        form.method = 'post';
        form.action = endpointFromTemplate(app.dataset.starUrlTemplate, experienceId);
        form.appendChild(createCsrfInput());

        const button = createElement('button', 'button button-star');
        button.type = 'submit';
        button.classList.toggle('is-starred', Boolean(experience.is_starred));
        button.setAttribute('aria-pressed', String(Boolean(experience.is_starred)));
        button.setAttribute(
            'aria-label',
            experience.is_starred
                ? `Batalkan star untuk ${experience.title}`
                : `Beri star untuk ${experience.title}`,
        );

        const starCount = Number.isFinite(Number(experience.star_count))
            ? Number(experience.star_count)
            : 0;
        button.title = starCount > 0
            ? `Dibintangi oleh ${experience.starred_by_names || ''}`
            : (IS_AUTHENTICATED
                ? 'Jadilah yang pertama memberi star'
                : 'Login untuk memberi star');

        const icon = createElement('span', '', '\u2605');
        icon.setAttribute('aria-hidden', 'true');
        button.append(icon, document.createTextNode(experience.is_starred ? ' Unstar ' : ' Star '));
        button.appendChild(createElement('span', 'star-count', starCount));
        form.appendChild(button);
        return form;
    }

    function buildExperienceCard(item) {
        const experience = item.fields;
        const article = createElement('article', 'experience-card');
        const thumbnailUrl = safeWebUrl(experience.thumbnail);

        if (thumbnailUrl) {
            const image = createElement('img', 'experience-thumbnail');
            image.src = thumbnailUrl;
            image.alt = experience.title;
            image.loading = 'lazy';
            article.appendChild(image);
        }

        article.appendChild(createElement('span', 'experience-category', experience.category_display));
        article.appendChild(createElement('h2', '', experience.title));
        article.appendChild(createElement('p', 'experience-description', experience.description));
        article.appendChild(createElement(
            'p',
            'experience-status',
            experience.is_ongoing ? 'Sedang berlangsung' : 'Selesai',
        ));

        const actions = createElement('div', 'experience-actions');
        actions.appendChild(buildStarForm(experience, item.pk));

        if (CAN_EDIT) {
            const editLink = createElement('a', 'button button-secondary', 'Ubah');
            editLink.href = endpointFromTemplate(app.dataset.editUrlTemplate, item.pk);
            actions.appendChild(editLink);
        }

        if (CAN_DELETE) {
            const deleteForm = createElement('form', 'experience-delete-form');
            deleteForm.method = 'post';
            deleteForm.action = endpointFromTemplate(app.dataset.deleteUrlTemplate, item.pk);
            deleteForm.appendChild(createCsrfInput());
            const deleteButton = createElement('button', 'button button-danger', 'Hapus');
            deleteButton.type = 'submit';
            deleteForm.appendChild(deleteButton);
            deleteForm.addEventListener('submit', (event) => {
                if (!window.confirm(`Yakin ingin menghapus experience "${experience.title}"?`)) {
                    event.preventDefault();
                }
            });
            actions.appendChild(deleteForm);
        }

        article.appendChild(actions);
        return article;
    }

    async function fetchExperiences(searchQuery = '') {
        requestController?.abort();
        requestController = new AbortController();

        try {
            setVisibleState({ loading: true });
            const url = new URL(app.dataset.listUrl, window.location.origin);
            if (searchQuery) url.searchParams.set('title', searchQuery);

            const response = await fetch(url, {
                headers: { Accept: 'application/json' },
                signal: requestController.signal,
            });
            if (!response.ok) throw new Error(`HTTP ${response.status}`);

            const experiences = await response.json();
            gridContainer.replaceChildren();
            if (experiences.length === 0) {
                emptyState.textContent = searchQuery
                    ? 'Tidak ada experience dengan judul tersebut.'
                    : 'Belum ada pengalaman yang ditambahkan.';
                setVisibleState({ empty: true });
                return;
            }

            experiences.forEach((item) => {
                gridContainer.appendChild(buildExperienceCard(item));
            });
            setVisibleState({ grid: true });
        } catch (error) {
            if (error.name === 'AbortError') return;
            console.error('Error loading experiences:', error);
            setVisibleState({ error: true });
        }
    }

    function runSearch() {
        fetchExperiences(searchInput.value.trim());
    }

    searchInput.addEventListener('input', () => {
        clearTimeout(searchTimer);
        searchTimer = setTimeout(runSearch, SEARCH_DEBOUNCE_DELAY);
    });

    searchForm.addEventListener('submit', (event) => {
        event.preventDefault();
        clearTimeout(searchTimer);
        runSearch();
    });

    async function addExperience(event) {
        event.preventDefault();
        const submitButton = experienceForm.querySelector('button[type="submit"]');
        submitButton.disabled = true;

        try {
            const response = await fetch(app.dataset.createUrl, {
                method: 'POST',
                headers: { 'X-CSRFToken': getCookie('csrftoken') },
                body: new FormData(experienceForm),
            });
            const result = await response.json().catch(() => ({}));

            if (response.ok) {
                experienceForm.reset();
                const modal = document.getElementById('add-experience-modal');
                if (modal?.matches(':popover-open')) modal.hidePopover();
                showToast('Berhasil', result.message || 'Experience berhasil ditambahkan.', 'success');
                await fetchExperiences(searchInput.value.trim());
                return;
            }

            const messages = result.errors
                ? Object.values(result.errors).flat().map((error) => error.message)
                : [result.message || `Terjadi kesalahan (status ${response.status}).`];
            showToast('Gagal menambahkan experience', messages.join(' '), 'error');
        } catch (error) {
            console.error('Error adding experience:', error);
            showToast(
                'Gagal menambahkan experience',
                'Tidak dapat terhubung ke server. Silakan coba lagi.',
                'error',
            );
        } finally {
            submitButton.disabled = false;
        }
    }

    experienceForm?.addEventListener('submit', addExperience);
    fetchExperiences(searchInput.value.trim());
})();
