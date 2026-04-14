let allFilms = [];
let watchedTitles = new Set();
let searchTimer = null;
let currentFilm = null;

const GENRE_EMOJI = {
    "Action": "💥", "Comedy": "😂", "Romance": "💕", "Thriller": "😰",
    "Horror": "👻", "Sci-Fi": "🚀", "Science Fiction": "🚀",
    "Fantasy": "🧙", "Documentary": "📽️", "Animation": "🎨",
    "Adventure": "🗺️", "Crime": "🕵️", "Mystery": "🔍",
    "Musical": "🎵", "Biography": "📖", "Drama": "🎭",
    "History": "📜", "War": "⚔️", "Western": "🤠", "Sport": "🏆",
    "Music": "🎶", "Family": "👨‍👩‍👧", "default": "🎬"
};

function getGenreEmoji(genres) {
    if (!genres || genres.length === 0) return "🎬";
    const trimmed = genres[0].trim();
    return GENRE_EMOJI[trimmed] || GENRE_EMOJI["default"];
}

// ===== INIT =====
document.addEventListener("DOMContentLoaded", async () => {
    await loadUser();
    await loadGenres();
    await loadYears();
    await loadFilms();
});

async function loadUser() {
    try {
        const res = await fetch("/api/user");
        const user = await res.json();
        document.getElementById("username-display").textContent = user.username;
        watchedTitles = new Set(Object.keys(user.watched_films || {}));
        updateBadge();
    } catch (e) {}
}

async function loadGenres() {
    try {
        const res = await fetch("/api/genres");
        const genres = await res.json();
        const sel = document.getElementById("genre-filter");
        genres.forEach(g => {
            const opt = document.createElement("option");
            opt.value = g.trim();
            opt.textContent = g.trim();
            sel.appendChild(opt);
        });
    } catch (e) {}
}

async function loadYears() {
    try {
        const res = await fetch("/api/years");
        const years = await res.json();
        const sel = document.getElementById("year-filter");
        years.forEach(y => {
            const opt = document.createElement("option");
            opt.value = y;
            opt.textContent = y;
            sel.appendChild(opt);
        });
    } catch (e) {}
}

async function loadFilms(params = {}) {
    const grid = document.getElementById("film-grid");
    grid.innerHTML = `<div class="loading"><div class="spinner"></div><p>Filmler yükleniyor...</p></div>`;
    try {
        const query = new URLSearchParams(params).toString();
        const res = await fetch("/api/films" + (query ? "?" + query : ""));
        allFilms = await res.json();
        renderFilms(allFilms);
    } catch (e) {
        grid.innerHTML = `<div class="empty-state"><span>⚠️</span><p>Filmler yüklenemedi.</p></div>`;
    }
}

function renderFilms(films) {
    const grid = document.getElementById("film-grid");
    document.getElementById("results-count").textContent = films.length + " film";

    if (films.length === 0) {
        grid.innerHTML = `<div class="empty-state"><span>🔍</span><p>Filtre ile eşleşen film bulunamadı.</p></div>`;
        return;
    }

    grid.innerHTML = films.map(f => filmCard(f)).join("");
}

function filmCard(film) {
    const emoji = getGenreEmoji(film.genres);
    const watched = watchedTitles.has(film.title);
    const genres = (film.genres || []).slice(0, 2).map(g =>
        `<span class="genre-tag">${g.trim()}</span>`
    ).join("");
    const score = film.score ? `<span class="card-score">⭐ ${film.score}</span>` : "";
    const year = film.release_year ? `<span class="card-year">${film.release_year}</span>` : "";
    const badge = watched ? `<span class="card-watched-badge">✓ İzledim</span>` : "";
    const safeTitle = escapeHtml(film.title);

    return `
    <div class="film-card" onclick="openModal('${safeTitle.replace(/'/g, "\\'")}')">
        <div class="card-poster">${emoji}${badge}</div>
        <div class="card-body">
            <div class="card-title">${safeTitle}</div>
            <div class="card-meta">${score}${year}</div>
            <div class="card-genres">${genres}</div>
        </div>
    </div>`;
}

// ===== FILTERS =====
function applyFilters() {
    const genre = document.getElementById("genre-filter").value;
    const score = document.getElementById("score-filter").value;
    const year = document.getElementById("year-filter").value;
    const search = document.getElementById("search-input").value.trim();
    const params = {};
    if (genre) params.genre = genre;
    if (score) params.min_score = score;
    if (year) params.year = year;
    if (search) params.search = search;
    loadFilms(params);
}

function clearFilters() {
    document.getElementById("genre-filter").value = "";
    document.getElementById("score-filter").value = "";
    document.getElementById("year-filter").value = "";
    document.getElementById("search-input").value = "";
    loadFilms();
}

function debounceSearch() {
    clearTimeout(searchTimer);
    searchTimer = setTimeout(applyFilters, 350);
}

// ===== PAGES =====
function showPage(name) {
    document.querySelectorAll(".page").forEach(p => p.classList.remove("active"));
    document.querySelectorAll(".nav-tab").forEach(t => t.classList.remove("active"));
    document.getElementById("page-" + name).classList.add("active");
    document.querySelectorAll(".nav-tab")[name === "browse" ? 0 : 1].classList.add("active");
    if (name === "watchlist") renderWatchlist();
}

// ===== WATCHLIST =====
async function renderWatchlist() {
    await loadUser();
    const grid = document.getElementById("watchlist-grid");
    const subtitle = document.getElementById("watchlist-subtitle");

    try {
        const res = await fetch("/api/user");
        const user = await res.json();
        const watched = user.watched_films || {};
        const entries = Object.entries(watched);
        subtitle.textContent = entries.length + " film";

        if (entries.length === 0) {
            grid.innerHTML = `<div class="empty-state">
                <span>🎭</span><p>Henüz izlenen film yok.</p>
                <button class="btn-primary" onclick="showPage('browse')">Film Keşfet</button>
            </div>`;
            return;
        }

        grid.innerHTML = entries.map(([title, data]) => {
            const film = data.film || {};
            const emoji = getGenreEmoji(film.genres);
            const score = film.score ? `<span class="card-score">⭐ ${film.score}</span>` : "";
            const year = film.release_year ? `<span class="card-year">${film.release_year}</span>` : "";
            const rating = data.rating != null ? `<span class="card-score">👤 ${data.rating}</span>` : "";
            const genres = (film.genres || []).slice(0, 2).map(g =>
                `<span class="genre-tag">${g.trim()}</span>`).join("");
            const safeTitle = escapeHtml(title);

            return `
            <div class="film-card" onclick="openModal('${safeTitle.replace(/'/g, "\\'")}', true)">
                <div class="card-poster">${emoji}<span class="card-watched-badge">✓ İzledim</span></div>
                <div class="card-body">
                    <div class="card-title">${safeTitle}</div>
                    <div class="card-meta">${score}${year}${rating}</div>
                    <div class="card-genres">${genres}</div>
                </div>
            </div>`;
        }).join("");
    } catch (e) {}
}

// ===== MODAL =====
async function openModal(title, fromWatchlist = false) {
    // Try to find in allFilms, otherwise fetch user data
    let film = allFilms.find(f => f.title === title);

    if (!film) {
        try {
            const res = await fetch("/api/user");
            const user = await res.json();
            const entry = user.watched_films[title];
            if (entry) film = entry.film;
        } catch (e) {}
    }

    if (!film) return;
    currentFilm = film;

    const watched = watchedTitles.has(film.title);
    const emoji = getGenreEmoji(film.genres);
    const genres = (film.genres || []).map(g =>
        `<span class="genre-tag">${g.trim()}</span>`).join("");
    const cast = (film.cast || []).map(a =>
        `<span class="cast-tag">${escapeHtml(a)}</span>`).join("");

    let reviewSection = "";
    if (watched) {
        const res = await fetch("/api/user");
        const user = await res.json();
        const entry = user.watched_films[film.title] || {};
        const hasReview = entry.rating != null;

        reviewSection = `
        <div class="review-section">
            <h4>📝 Değerlendirmem</h4>
            <div id="review-content">
                ${hasReview ? savedReviewHTML(entry) : reviewFormHTML(film.title, "", "")}
            </div>
        </div>`;
    }

    document.getElementById("modal-body").innerHTML = `
        <div class="modal-poster">${emoji}</div>
        <div class="modal-title">${escapeHtml(film.title)}</div>
        <div class="modal-director">🎬 ${escapeHtml(film.director || "Bilinmiyor")}</div>
        <div class="modal-stats">
            ${film.score ? `<span class="stat-pill gold">⭐ ${film.score}</span>` : ""}
            ${film.release_year ? `<span class="stat-pill">📅 ${film.release_year}</span>` : ""}
            ${film.duration ? `<span class="stat-pill">⏱️ ${film.duration} dk</span>` : ""}
            ${film.language ? `<span class="stat-pill">🌐 ${film.language}</span>` : ""}
        </div>
        <div class="modal-genres">${genres}</div>
        ${film.description ? `<div class="modal-description">${escapeHtml(film.description)}</div>` : ""}
        ${cast ? `<div class="modal-cast"><h4>Oyuncular</h4><div class="cast-list">${cast}</div></div>` : ""}
        <div class="modal-actions">
            ${watched
                ? `<button class="btn-danger btn-sm" onclick="unwatch('${escapeHtml(film.title).replace(/'/g, "\\'")}')">✕ İzlenenlerden Çıkar</button>`
                : `<button class="btn-primary btn-sm" onclick="markWatched('${escapeHtml(film.title).replace(/'/g, "\\'")}')">✓ İzledim</button>`
            }
        </div>
        ${reviewSection}
    `;

    document.getElementById("modal-overlay").classList.add("open");
    document.body.style.overflow = "hidden";
}

function savedReviewHTML(entry) {
    return `<div class="saved-review">
        <div class="r-score">⭐ Puanım: ${entry.rating}/10</div>
        ${entry.review ? `<div class="r-text">"${escapeHtml(entry.review)}"</div>` : ""}
        <button class="btn-secondary btn-sm" style="margin-top:10px"
            onclick="editReview('${escapeHtml(entry.review || "")}', ${entry.rating})">Düzenle</button>
    </div>`;
}

function reviewFormHTML(title, existingReview, existingRating) {
    return `<div class="review-form">
        <div class="score-input-row">
            <label>Puanım (0-10):</label>
            <input type="number" id="rating-input" min="0" max="10" step="0.5"
                value="${existingRating || ""}" placeholder="8.5">
        </div>
        <textarea id="review-input" placeholder="Yorumunuzu yazın...">${existingReview || ""}</textarea>
        <button class="btn-primary btn-sm" onclick="submitReview('${escapeHtml(title).replace(/'/g, "\\'")}')">Kaydet</button>
    </div>`;
}

function editReview(existingReview, existingRating) {
    if (!currentFilm) return;
    document.getElementById("review-content").innerHTML =
        reviewFormHTML(currentFilm.title, existingReview, existingRating);
}

function closeModal(event) {
    if (event.target === document.getElementById("modal-overlay")) closeModalDirect();
}

function closeModalDirect() {
    document.getElementById("modal-overlay").classList.remove("open");
    document.body.style.overflow = "";
    currentFilm = null;
}

// ===== WATCH ACTIONS =====
async function markWatched(title) {
    const film = allFilms.find(f => f.title === title) || currentFilm;
    if (!film) return;
    try {
        const res = await fetch("/api/watch", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ title, film })
        });
        const data = await res.json();
        watchedTitles.add(title);
        updateBadge();
        showToast(data.message, "success");
        closeModalDirect();
        renderFilms(allFilms);
    } catch (e) { showToast("Bir hata oluştu.", "error"); }
}

async function unwatch(title) {
    try {
        const res = await fetch("/api/unwatch", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ title })
        });
        const data = await res.json();
        watchedTitles.delete(title);
        updateBadge();
        showToast(data.message, "success");
        closeModalDirect();
        renderFilms(allFilms);
        renderWatchlist();
    } catch (e) { showToast("Bir hata oluştu.", "error"); }
}

async function submitReview(title) {
    const rating = document.getElementById("rating-input")?.value;
    const review = document.getElementById("review-input")?.value;
    try {
        const res = await fetch("/api/review", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ title, rating: parseFloat(rating), review })
        });
        const data = await res.json();
        if (res.ok) {
            showToast(data.message, "success");
            document.getElementById("review-content").innerHTML =
                savedReviewHTML({ rating: parseFloat(rating), review });
        } else {
            showToast(data.message, "error");
        }
    } catch (e) { showToast("Bir hata oluştu.", "error"); }
}

// ===== UTILITIES =====
function updateBadge() {
    const badge = document.getElementById("watched-badge");
    badge.textContent = watchedTitles.size;
}

function showToast(msg, type = "") {
    const toast = document.getElementById("toast");
    toast.textContent = msg;
    toast.className = "toast show " + type;
    setTimeout(() => { toast.className = "toast"; }, 3000);
}

function escapeHtml(str) {
    if (!str) return "";
    return String(str)
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;");
}
