button_btn = document.querySelector(".button-btn")

button_btn.onclick = function() {
    this.innerHTML = "<div class='loader'></div>";
    setTimeout(() => {
        this.innerHTML = "Error :)";
        this.style = "background: #ff7200; color: #fff; pointer-events: none";
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

/* Type */

const selected = document.querySelector(".selected");
const optionsContainer = document.querySelector(".options-container");

const optionsList = document.querySelectorAll(".option");

selected.addEventListener("click", () => {
    optionsContainer.classList.toggle("active");
});

optionsList.forEach(o => {
    o.addEventListener("click", () => {
      selected.innerHTML = o.querySelector("label").innerHTML;
      optionsContainer.classList.remove("active");
    });
});


/* Product Cards */

class TabbedContent {
    constructor() {
      this.tabs = document.querySelectorAll(".nav li");
      this.sections = document.querySelectorAll(".section");
      this.nextButton = document.querySelector("#nextBtn");
      this.prevButton = document.querySelector("#prevBtn");
      this.current = 0;
    }
  
    toggleTabs() {
      this.tabs.forEach(function(tab) {
        tab.classList.remove('active');
      });
      this.tabs[this.current].classList.add("active");
    }
  
    toggleSections() {
      this.sections.forEach(function(section) {
        section.classList.remove('active');
      });
      this.sections[this.current].classList.add("active");
    }
  
    togglePrev() {
      const method = this.current == 0 ? 'add' : 'remove';
      this.prevButton.classList[method]("disable");
    }
  
    toggleNext() {
      const method = this.current == this.tabs.length - 1 ? 'add' : 'remove';
      this.nextButton.classList[method]("disable");
    }
  
    goNext() {
      if (this.current < this.tabs.length - 1) {
        this.current++
      }
      this.toggleTabs();
      this.toggleSections();
      this.toggleNext();
      this.togglePrev();
    }
  
    goPrev() {
      if (this.current > 0) {
        this.current--
      }
      this.toggleTabs();
      this.toggleSections();
      this.toggleNext();
      this.togglePrev();
    }
}
  
const tabbedContent = new TabbedContent();
