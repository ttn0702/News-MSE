let currentArticles = [];
let currentIndex = 0;
const domainBE = "http://127.0.0.1:1111"
const defaultImageUrl = 'https://via.placeholder.com/400x300?text=No+Image+Available';

// Function to fetch categories and populate the navigation bar
async function loadCategories() {
    try {
        const response = await fetch(`${domainBE}/api/category`);
        const categories = await response.json();
        const nav = document.getElementById('nav');

        // Clear existing nav items
        nav.innerHTML = '';

        // Add categories to nav bar
        for (const key in categories) {
            if (categories.hasOwnProperty(key)) {
                const category = categories[key];
                const anchor = document.createElement('a');
                anchor.href = "#";
                anchor.innerText = category.name;
                anchor.dataset.url = category.url;  // Store the URL in a data attribute
                anchor.onclick = () => fetchArticles(category.url);
                nav.appendChild(anchor);
            }
        }

        // Set the first item as active
        if (nav.firstChild) {
            nav.firstChild.classList.add('active');
            fetchArticles(nav.firstChild.dataset.url);
        }

    } catch (error) {
        console.error('Error fetching categories:', error);
    }
}

// Function to fetch articles based on category URL
async function fetchArticles(url) {
    try {
        const response = await fetch(`${domainBE}/api/get_article?url=${encodeURIComponent(url)}`);
        const result = await response.json();
        currentArticles = result.data;
        currentIndex = 0;
        updateContent(currentArticles[currentIndex]);

        // Enable or disable buttons based on the number of articles
        updateNavigationButtons();

        // Set the clicked category as active
        document.querySelectorAll('.nav a').forEach(anchor => {
            anchor.classList.remove('active');
        });
        document.querySelector(`.nav a[data-url='${url}']`).classList.add('active');

    } catch (error) {
        console.error('Error fetching articles:', error);
    }
}

// Function to update the content area with a specific article
function updateContent(article) {
    const content = document.getElementById('content');
    if (article) {
        const imageUrl = article.image_link || defaultImageUrl;
        content.innerHTML = `
            <h2>${article.title}</h2>
            <div class="author">${new Date(article.published).toLocaleDateString()}</div>
            <p>${article.description}</p>
            <img src="${imageUrl}" alt="${article.title}">
        `;

        // Update the Read More button to open the current article's URL
        const readMoreButton = document.getElementById('read-more');
        readMoreButton.dataset.url = article.url;
    } else {
        content.innerHTML = '<p>No articles available for this category.</p>';
    }
}

// Function to handle the Next Article button click
function nextArticle() {
    if (currentIndex < currentArticles.length - 1) {
        currentIndex++;
        updateContent(currentArticles[currentIndex]);
        updateNavigationButtons();
    }
}

// Function to handle the Previous Article button click
function prevArticle() {
    if (currentIndex > 0) {
        currentIndex--;
        updateContent(currentArticles[currentIndex]);
        updateNavigationButtons();
    }
}

// Function to update the state of the navigation buttons
function updateNavigationButtons() {
    const prevButton = document.getElementById('prev-article');
    const nextButton = document.getElementById('next-article');

    prevButton.disabled = currentIndex === 0;
    nextButton.disabled = currentIndex === currentArticles.length - 1;
}

// Function to handle the Read More button click
function readMore() {
    const readMoreButton = document.getElementById('read-more');
    const url = readMoreButton.dataset.url;
    if (url) {
        window.open(url, '_blank');  // Open the URL in a new tab
    }
}

// Load categories when the page loads
window.onload = loadCategories;

// Add horizontal scroll with mouse wheel to the navigation bar
const navContainer = document.getElementById('nav-container');
navContainer.addEventListener('wheel', function(event) {
    if (event.deltaY > 0) {
        navContainer.scrollLeft += 100;
    } else {
        navContainer.scrollLeft -= 100;
    }
});
