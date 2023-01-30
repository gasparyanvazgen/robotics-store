button_btn = document.querySelector('.button-btn')

button_btn.onclick = function() {
    this.innerHTML = '<div class="loader"></div>';
    setTimeout(() => {
        this.innerHTML = 'Error :)';
        this.style = 'background: #ff7200; color: #fff; pointer-events: none';
    }, 5000);
}


const links = document.querySelectorAll('.scroll-btn');

for (const link of links) {
    link.addEventListener('click', clickHandlear);
}

function clickHandlear(e) {
    e.preventDefault();
    const href = this.getAttribute('href');
    const offsetTop = document.querySelector(href).
    offsetTop;

    scroll({
        top: offsetTop,
        behavior: 'smooth'
    });
}

// Type

const selected = document.querySelector('.selected');
const optionsContainer = document.querySelector('.options-container');

const optionsList = document.querySelectorAll('.option');

selected.addEventListener('click', () => {
  optionsContainer.classList.toggle('active');
});

optionsList.forEach(o => {
  o.addEventListener('click', () => {
    selected.innerHTML = o.querySelector('label').innerHTML;
    optionsContainer.classList.remove('active');
  });
});
