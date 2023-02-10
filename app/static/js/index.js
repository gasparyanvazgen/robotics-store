function doSomething(){
  document.getElementById("test").innerHTML = "Գնումներ կարող եք կատարել զանգի կամ հաղորդագրության միջոցով:Կայքի Ներքևի հատվածում կարող եք  գտնել ձեզ անհրաժեշտ ապրանքները և դրանց գները";
}

// Type - categories
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
