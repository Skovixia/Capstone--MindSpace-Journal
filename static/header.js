document.addEventListener('DOMContentLoaded', function() {
    const header = document.createElement('header');
    header.classList.add('header');

    const logoLink = document.createElement('a');
    logoLink.href = urls.indexUrl;  // Accessing the injected index URL
    logoLink.classList.add('logo');
    logoLink.textContent = "MindSpace";

    header.appendChild(logoLink);

    const nav = document.createElement('nav');
    nav.classList.add('navbar');

    const links = [
        { text: 'Journal', url: urls.indexUrl },
        { text: 'Visuals/Datasets', url: urls.visualsUrl},
        { text: 'About', url: urls.aboutUrl}
    ];

    links.forEach(link => {
        const a = document.createElement('a');
        a.href = link.url;
        a.textContent = link.text;
        nav.appendChild(a);
    });

    header.appendChild(nav);

    document.body.insertBefore(header, document.body.firstChild);
});
