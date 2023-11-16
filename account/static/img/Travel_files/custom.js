document.addEventListener("DOMContentLoaded", (event) => {
  document
    .querySelector("#arrival-search-btn")
    .addEventListener("click", (event) => {
      event.preventDefault();
      const arrivalToCity = document.querySelector("#arrival-to-city").value;
      window.location.href = `/flights/arr/${arrivalToCity}/`;
    });
});
