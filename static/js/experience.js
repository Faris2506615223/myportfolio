(() => {
    const app = document.getElementById('experience-app');
    if (!app) return;

    const { getCookie, safeWebUrl } = window.ajaxUtils;
    const SEARCH_DEBOUNCE_DELAY = 300;
    const UUID_PLACEHOLDER = '00000000-0000-0000-0000-000000000000';
    const IS_AUTHENTICATED = app.dataset.isAuthenticated === 'true';
    const CAN_EDIT = app.dataset.canEdit === 'true';
    const CAN_DELETE = app.dataset.canDelete === 'true';
    const FIELD_LABELS = {
        title: 'Posisi / Kegiatan', description: 'Deskripsi',
        category: 'Kategori', thumbnail: 'URL Thumbnail',
    };
    const loadingState = document.getElementById('experience-loading');
    const errorState = document.getElementById('experience-error');
    const emptyState = document.getElementById('experience-empty');
    const gridContainer = document.getElementById('experience-grid');
    const resultCount = document.getElementById('experience-result-count');
    const searchForm = document.getElementById('experience-search-form');
    const searchInput = document.getElementById('experience-search-input');
    const categoryFilter = document.getElementById('experience-category-filter');
    const statusFilter = document.getElementById('experience-status-filter');
    const experienceForm = document.getElementById('experience-form');
    const editForm = document.getElementById('experience-edit-form');
    let requestController;
    let searchTimer;
    let editLoading = false;

    function createElement(tagName, className, text) {
        const element = document.createElement(tagName);
        if (className) element.className = className;
        if (text !== undefined) element.textContent = String(text);
        return element;
    }

    function endpointFromTemplate(template, id) {
        return template.replace(UUID_PLACEHOLDER, encodeURIComponent(id));
    }

    function detailEndpoint(id) {
        return endpointFromTemplate(app.dataset.detailUrlTemplate, id);
    }

    function errorMessages(data) {
        if (Array.isArray(data)) return data.flatMap(errorMessages);
        if (data && typeof data === 'object') {
            return Object.entries(data).flatMap(([key, value]) => {
                const messages = errorMessages(value);
                return FIELD_LABELS[key]
                    ? messages.map((message) => `${FIELD_LABELS[key]}: ${message}`)
                    : messages;
            });
        }
        return data ? [String(data)] : [];
    }

    // All writes share the same session, CSRF and DRF error handling.
    // A 204 response deliberately has no body to parse.
    async function apiRequest(url, { method = 'GET', data, signal } = {}) {
        const headers = { Accept: 'application/json' };
        if (!['GET', 'HEAD', 'OPTIONS'].includes(method)) {
            headers['X-CSRFToken'] = getCookie('csrftoken') || '';
        }
        if (data !== undefined) headers['Content-Type'] = 'application/json';
        const response = await fetch(url, {
            method, headers, credentials: 'same-origin', signal,
            body: data === undefined ? undefined : JSON.stringify(data),
        });
        const result = response.status === 204
            ? null : await response.json().catch(() => null);
        if (!response.ok) {
            const messages = errorMessages(result);
            const error = new Error(messages.join(' ') || `Permintaan gagal (HTTP ${response.status}).`);
            error.fields = result;
            throw error;
        }
        return result;
    }

    function notifyError(title, error) {
        showToast(title, error.message || 'Tidak dapat terhubung ke server. Silakan coba lagi.', 'error');
    }

    function setVisibleState({ loading = false, error = false, empty = false, grid = false }) {
        loadingState.classList.toggle('hide', !loading);
        errorState.classList.toggle('hide', !error);
        emptyState.classList.toggle('hide', !empty);
        gridContainer.classList.toggle('hide', !grid);
        gridContainer.setAttribute('aria-busy', String(loading));
        if (loading || error) resultCount.textContent = '';
    }

    async function withBusyButton(button, action) {
        if (button.disabled) return;
        button.disabled = true;
        try {
            await action();
        } catch (error) {
            notifyError('Permintaan gagal', error);
        } finally {
            button.disabled = false;
        }
    }

    function buildStarButton(experience, article) {
        const button = createElement(IS_AUTHENTICATED ? 'button' : 'a', 'button button-star');
        if (IS_AUTHENTICATED) {
            button.type = 'button';
            button.setAttribute('aria-pressed', String(experience.is_starred));
            button.addEventListener('click', () => withBusyButton(button, async () => {
                const updated = await apiRequest(
                    endpointFromTemplate(app.dataset.starUrlTemplate, experience.id),
                    { method: 'POST' },
                );
                const newCard = buildExperienceCard(updated);
                article.replaceWith(newCard);
                newCard.querySelector('.button-star').focus({ preventScroll: true });
                showToast('Berhasil', updated.is_starred ? 'Star ditambahkan.' : 'Star dibatalkan.', 'success');
            }));
        } else {
            button.href = app.dataset.loginUrl;
        }
        button.classList.toggle('is-starred', Boolean(experience.is_starred));
        button.setAttribute('aria-label', experience.is_starred
            ? `Batalkan star untuk ${experience.title}` : `Beri star untuk ${experience.title}`);
        button.title = experience.star_count > 0
            ? `Dibintangi oleh ${experience.starred_by_names}`
            : (IS_AUTHENTICATED ? 'Jadilah yang pertama memberi star' : 'Login untuk memberi star');
        const icon = createElement('span', '', '\u2605');
        icon.setAttribute('aria-hidden', 'true');
        button.append(icon, document.createTextNode(experience.is_starred ? ' Unstar ' : ' Star '));
        button.appendChild(createElement('span', 'star-count', experience.star_count));
        return button;
    }

    function clearFormErrors(form) {
        form.querySelectorAll('.field-error').forEach((node) => { node.textContent = ''; });
        form.querySelectorAll('[aria-invalid]').forEach((node) => node.removeAttribute('aria-invalid'));
        form.querySelector('.form-feedback').classList.add('hide');
    }

    function displayFormErrors(form, error) {
        const feedback = form.querySelector('.form-feedback');
        feedback.textContent = error.message;
        feedback.classList.remove('hide');
        Object.entries(error.fields || {}).forEach(([name, messages]) => {
            const input = form.elements.namedItem(name);
            if (!input?.id) return;
            input.setAttribute('aria-invalid', 'true');
            input.setAttribute('aria-describedby', `${input.id}_error`);
            document.getElementById(`${input.id}_error`).textContent = errorMessages(messages).join(' ');
        });
        form.querySelector('[aria-invalid="true"]')?.focus();
    }

    async function openEdit(experienceId) {
        if (editLoading || editForm.dataset.busy === 'true') return;
        editLoading = true;
        try {
            const experience = await apiRequest(detailEndpoint(experienceId));
            clearFormErrors(editForm);
            editForm.reset();
            Object.keys(FIELD_LABELS).forEach((name) => {
                editForm.elements.namedItem(name).value = experience[name] || '';
            });
            editForm.dataset.experienceId = experience.id;
            const modal = document.getElementById('edit-experience-modal');
            if (!modal.matches(':popover-open')) modal.showPopover();
            editForm.elements.namedItem('title').focus();
        } finally {
            editLoading = false;
        }
    }

    function buildExperienceCard(experience) {
        const article = createElement('article', 'experience-card');
        const thumbnailUrl = safeWebUrl(experience.thumbnail);
        if (thumbnailUrl) {
            const image = createElement('img', 'experience-thumbnail');
            image.src = thumbnailUrl;
            image.alt = experience.title;
            image.loading = 'lazy';
            image.addEventListener('error', () => image.remove(), { once: true });
            article.appendChild(image);
        }
        article.appendChild(createElement('span', 'experience-category', experience.category_display));
        article.appendChild(createElement('h2', '', experience.title));
        article.appendChild(createElement('p', 'experience-description', experience.description));
        article.appendChild(createElement('p', 'experience-status',
            experience.is_ongoing ? 'Sedang berlangsung' : 'Selesai'));
        const actions = createElement('div', 'experience-actions');
        actions.appendChild(buildStarButton(experience, article));
        if (CAN_EDIT) {
            const editButton = createElement('button', 'button button-secondary', 'Ubah');
            editButton.type = 'button';
            editButton.addEventListener('click', () => withBusyButton(editButton, () => openEdit(experience.id)));
            actions.appendChild(editButton);
        }
        if (CAN_DELETE) {
            const deleteButton = createElement('button', 'button button-danger', 'Hapus');
            deleteButton.type = 'button';
            deleteButton.addEventListener('click', () => {
                if (!window.confirm(`Yakin ingin menghapus experience "${experience.title}"?`)) return;
                withBusyButton(deleteButton, async () => {
                    await apiRequest(detailEndpoint(experience.id), { method: 'DELETE' });
                    showToast('Berhasil', 'Experience berhasil dihapus.', 'success');
                    await fetchExperiences(searchInput.value.trim());
                });
            });
            actions.appendChild(deleteButton);
        }
        article.appendChild(actions);
        return article;
    }

    function filterParams(searchQuery) {
        const params = new URLSearchParams();
        if (searchQuery) params.set('title', searchQuery);
        if (categoryFilter.value) params.set('category', categoryFilter.value);
        if (statusFilter.value) params.set('status', statusFilter.value);
        return params;
    }

    async function fetchExperiences(searchQuery = '') {
        requestController?.abort();
        const controller = new AbortController();
        requestController = controller;
        setVisibleState({ loading: true });
        try {
            const url = new URL(app.dataset.listUrl, window.location.origin);
            url.search = filterParams(searchQuery).toString();
            const experiences = await apiRequest(url, { signal: controller.signal });
            if (controller.signal.aborted) return;
            gridContainer.replaceChildren(...experiences.map(buildExperienceCard));
            resultCount.textContent = `${experiences.length} experience ditampilkan`;
            emptyState.textContent = filterParams(searchQuery).size
                ? 'Tidak ada experience yang cocok. Coba kata kunci atau filter lain.'
                : 'Belum ada pengalaman yang ditambahkan.';
            setVisibleState({ empty: experiences.length === 0, grid: experiences.length > 0 });
        } catch (error) {
            if (controller.signal.aborted) return;
            setVisibleState({ error: true });
            notifyError('Gagal memuat experience', error);
        }
    }

    function runSearch() {
        const url = new URL(window.location.href);
        url.search = filterParams(searchInput.value.trim()).toString();
        window.history.replaceState(null, '', url);
        fetchExperiences(searchInput.value.trim());
    }

    searchInput.addEventListener('input', () => {
        clearTimeout(searchTimer);
        requestController?.abort();
        searchTimer = setTimeout(runSearch, SEARCH_DEBOUNCE_DELAY);
    });
    searchForm.addEventListener('submit', (event) => {
        event.preventDefault();
        clearTimeout(searchTimer);
        runSearch();
    });
    [categoryFilter, statusFilter].forEach((filter) => filter.addEventListener('change', () => {
        clearTimeout(searchTimer);
        runSearch();
    }));
    document.getElementById('experience-reset').addEventListener('click', () => {
        clearTimeout(searchTimer);
        searchInput.value = '';
        categoryFilter.value = '';
        statusFilter.value = '';
        runSearch();
    });
    document.getElementById('experience-retry').addEventListener('click', runSearch);

    async function saveExperience(event, isEdit) {
        event.preventDefault();
        const form = event.currentTarget;
        if (form.dataset.busy === 'true') return;
        form.dataset.busy = 'true';
        const submitButton = form.querySelector('button[type="submit"]');
        submitButton.disabled = true;
        const originalLabel = submitButton.textContent;
        submitButton.textContent = 'Menyimpan...';
        clearFormErrors(form);
        try {
            const payload = Object.fromEntries(Object.keys(FIELD_LABELS).map((name) =>
                [name, form.elements.namedItem(name).value]));
            await apiRequest(isEdit ? detailEndpoint(form.dataset.experienceId) : app.dataset.listUrl, {
                method: isEdit ? 'PATCH' : 'POST', data: payload,
            });
            const modal = form.closest('[popover]');
            if (modal.matches(':popover-open')) modal.hidePopover();
            form.reset();
            showToast('Berhasil', isEdit ? 'Experience diperbarui.' : 'Experience ditambahkan.', 'success');
            await fetchExperiences(searchInput.value.trim());
        } catch (error) {
            displayFormErrors(form, error);
            notifyError('Gagal menyimpan experience', error);
        } finally {
            form.dataset.busy = 'false';
            submitButton.disabled = false;
            submitButton.textContent = originalLabel;
        }
    }

    experienceForm?.addEventListener('submit', (event) => saveExperience(event, false));
    editForm?.addEventListener('submit', (event) => saveExperience(event, true));
    const initialParams = new URLSearchParams(window.location.search);
    categoryFilter.value = initialParams.get('category') || '';
    statusFilter.value = initialParams.get('status') || '';
    fetchExperiences(searchInput.value.trim());
})();
