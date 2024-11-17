const kategoriDropdown = document.querySelector("#kategori-dropdown");
const subkategoriDropdown = document.querySelector("#subkategori-dropdown");
const optionTemplateRef = document.querySelector("#option-template");
const resultsContainer = document.querySelector("#results");
const resultTemplateRef = document.querySelector("#result-template");

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

async function handleSearch() {
  const subcategory = subkategoriDropdown.value;
  const response = await fetch(
    "/pekerjaan_jasa/get_tickets/?" +
      new URLSearchParams({ subkategori: subcategory })
  );
  const jsonData = await response.json();

  resultsContainer.replaceChildren();

  jsonData.data.forEach((ticket) => {
    let clone = resultTemplateRef.content.cloneNode(true);

    let subkategoriPesananEle = clone.querySelector("#subkategori-pesanan");
    let namaPelangganEle = clone.querySelector("#nama-pelanggan");
    let tanggalPemesananEle = clone.querySelector("#tanggal-pemesanan");
    let tanggalPekerjaanEle = clone.querySelector("#tanggal-pekerjaan");
    let biayaEle = clone.querySelector("#biaya");

    subkategoriPesananEle.innerHTML = ticket.subkategori
      .split("_")
      .map((w) => w[0].toUpperCase() + w.substring(1).toLowerCase())
      .join(" ");
    namaPelangganEle.innerHTML = ticket.nama_pelanggan;
    tanggalPemesananEle.innerHTML = ticket.tanggal_pemesanan;
    tanggalPekerjaanEle.innerHTML = ticket.tanggal_pekerjaan;
    biayaEle.innerHTML = ticket.biaya;

    resultsContainer.appendChild(clone);
  });
}

window.onload = () => {
  fetchCategories();
};
