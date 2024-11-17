const kategoriDropdown = document.querySelector("#kategori-dropdown");
const subkategoriDropdown = document.querySelector("#subkategori-dropdown");
const optionTemplateRef = document.querySelector("#option-template");

async function fetchCategories() {
  const response = await fetch("/pekerjaan_jasa/get_kategori");
  const jsonData = await response.json();

  jsonData.data.forEach((category) => {
    let clone = optionTemplateRef.content.cloneNode(true);
    let optionEle = clone.querySelector("option");

    optionEle.value = category.toLowerCase().replace(" ", "_");
    optionEle.innerHTML = category;

    kategoriDropdown.appendChild(clone);
  });
}

async function handleCategoryChange(category) {
  // Let form input persist as long as window isn't closed
  sessionStorage.setItem("kategori", category);

  const response = await fetch(
    "/pekerjaan_jasa/get_subkategori/?" +
      new URLSearchParams({ kategori: category })
  );
  const jsonData = await response.json();

  subkategoriDropdown.replaceChildren();

  jsonData.data.forEach((subcategory) => {
    let clone = optionTemplateRef.content.cloneNode(true);
    let optionEle = clone.querySelector("option");

    optionEle.value = subcategory.toLowerCase().replace(" ", "_");
    optionEle.innerHTML = subcategory;

    subkategoriDropdown.appendChild(clone);
  });
}

async function handleSubcategoryChange(subcategory) {
  const response = await fetch();
}

window.onload = () => {
  sessionStorage.getItem("kategori");
  fetchCategories();
};
