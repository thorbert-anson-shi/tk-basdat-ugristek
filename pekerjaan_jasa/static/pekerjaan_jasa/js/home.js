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

    optionEle.value = category[1];
    optionEle.innerHTML = category[0];

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

    optionEle.value = subcategory[1];
    optionEle.innerHTML = subcategory[0];

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
    let takeButton = clone.querySelector("#take-ticket-btn");

    subkategoriPesananEle.innerHTML = ticket.subkategori;
    namaPelangganEle.innerHTML = ticket.nama_pelanggan;
    tanggalPemesananEle.innerHTML = ticket.tanggal_pemesanan;
    tanggalPekerjaanEle.innerHTML = ticket.tanggal_pekerjaan;
    biayaEle.innerHTML = ticket.biaya;
    takeButton.onclick = () => handleTakeTicket(ticket.id);

    resultsContainer.appendChild(clone);
  });
}

async function handleTakeTicket(ticketId) {
  const response = await fetch(
    "/pekerjaan_jasa/take_ticket/?" +
      new URLSearchParams({ ticket_id: ticketId })
  );
  const jsonData = await response.json();

  if (jsonData.success) {
    alert("Berhasil mengambil pesanan!");
  } else {
    alert("Gagal mengambil pesanan!");
  }

  handleSearch();
}

window.onload = () => {
  fetchCategories();
};
