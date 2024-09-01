document.addEventListener('DOMContentLoaded', () => {
    const themeIcon = document.getElementById('themeIcon');
    const currentTheme = localStorage.getItem('theme') || 'light';
    const container = document.querySelector('.container');
    const h1 = document.querySelector('h1');
    const footer = document.querySelector('footer');
    const table = document.querySelector('table');
    const thElements = document.querySelectorAll('th');
    const tdElements = document.querySelectorAll('td');
    const buttonElements = document.querySelectorAll('.button');

    if (currentTheme === 'dark') {
        document.body.classList.add('dark-theme');
        container.classList.add('dark-theme');
        h1.classList.add('dark-theme');
        footer.classList.add('dark-theme');
        table.classList.add('dark-theme');
        thElements.forEach(th => th.classList.add('dark-theme'));
        tdElements.forEach(td => td.classList.add('dark-theme'));
        buttonElements.forEach(button => button.classList.add('dark-theme'));
        themeIcon.src = 'moon.png';
    } else {
        themeIcon.src = 'sun.png';
    }

    themeIcon.addEventListener('click', () => {
        document.body.classList.toggle('dark-theme');
        container.classList.toggle('dark-theme');
        h1.classList.toggle('dark-theme');
        footer.classList.toggle('dark-theme');
        table.classList.toggle('dark-theme');
        thElements.forEach(th => th.classList.toggle('dark-theme'));
        tdElements.forEach(td => td.classList.toggle('dark-theme'));
        buttonElements.forEach(button => button.classList.toggle('dark-theme'));
        
        const theme = document.body.classList.contains('dark-theme') ? 'dark' : 'light';
        localStorage.setItem('theme', theme);

        themeIcon.src = theme === 'dark' ? 'moon.png' : 'sun.png';
    });
});
