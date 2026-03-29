function LoadComponent(url, containerId) {
    fetch(url)
    .then(function(response) {
        return response.text()
    })
    .then(function(data) {
        document.getElementById(containerId).innerHTML = data
    })
    .catch(function(error) {
        console.error('Ошибка загрузки компонента:', error);
    });
}

LoadComponent('menu.html', 'menu-container')
LoadComponent('footer.html', 'footer-container')
