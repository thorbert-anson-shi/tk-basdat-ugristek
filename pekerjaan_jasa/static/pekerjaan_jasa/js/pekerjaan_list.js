const statusDropdown = document.querySelector("#status-dropdown");
const resultTemplateRef = document.querySelector("#result-template");
const resultsContainer = document.querySelector("#results");
const optionTemplate = document.querySelector("#option-template");

async function handleSearch() {
  let status = statusDropdown.value;

  let endpoint = "/pekerjaan_jasa/get_tickets?";

  if (status != null) {
    endpoint += new URLSearchParams({ status: status });
  }

  const response = await fetch(endpoint);

  const jsonData = await response.json();

  resultsContainer.replaceChildren();

  jsonData.data.forEach((ticket) => {
    let clone = resultTemplateRef.content.cloneNode(true);

    let result = clone.querySelector("#result");
    let subkategoriPesananEle = clone.querySelector("#subkategori-pesanan");
    let namaPelangganEle = clone.querySelector("#nama-pelanggan");
    let tanggalPemesananEle = clone.querySelector("#tanggal-pemesanan");
    let tanggalPekerjaanEle = clone.querySelector("#tanggal-pekerjaan");
    let biayaEle = clone.querySelector("#biaya");
    let statusPemesanan = clone.querySelector("#status-pemesanan");
    let statusUpdateButton = clone.querySelector("#status-update-button");

    result.setAttribute("data-ticketId", ticket.id);
    subkategoriPesananEle.innerHTML = ticket.subkategori
      .split("_")
      .map((w) => w[0].toUpperCase() + w.substring(1).toLowerCase())
      .join(" ");
    namaPelangganEle.innerHTML = ticket.nama_pelanggan;
    tanggalPemesananEle.innerHTML = ticket.tanggal_pemesanan;
    tanggalPekerjaanEle.innerHTML = ticket.tanggal_pekerjaan;
    biayaEle.innerHTML = ticket.biaya;
    statusPemesanan.innerHTML = ticket.status;

    if (ticket.status != "Selesai Melakukan Pelayanan") {
      statusUpdateButton.setAttribute("data-ticketId", ticket.id);
      statusUpdateButton.style.display = "block";
    } else {
      statusUpdateButton.style.display = "none";
    }

    resultsContainer.appendChild(clone);
  });
}

async function handleStatusUpdate(ticketId) {
  let response = await fetch("/pekerjaan_jasa/update_ticket_status/", {
    method: "POST",
    body: JSON.stringify({ id: ticketId }),
  });

  if (response.status == 200) {
    document.querySelector(`div[data-ticketid='${ticketId}']`).remove();
  }
}

window.onload = async () => {
  let response = await fetch("/pekerjaan_jasa/get_status_choices");
  let statuses = await response.json();

  statuses.choices.forEach((choice) => {
    let clone = optionTemplate.content.cloneNode(true);

    optionEle = clone.querySelector("option");

    optionEle.innerHTML = choice[1];
    optionEle.value = choice[0];

    statusDropdown.appendChild(clone);
  });
};
