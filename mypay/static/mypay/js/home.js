const scrollContainer = document.querySelector("#scroll-container");
const template = document.querySelector("#transaction-item");
const transactionModal = document.querySelector("#transaction-modal");
const transactionEndpoint = "/transactions/";

function handleCreateTransaction() {
  transactionModal.showModal();
}

function renderTransactions() {
  // Empty table before each rerender
  scrollContainer.replaceChildren();

  const transactions = [
    { nominal: 200, tanggal: "2024-12-21", kategori: "good" },
    { nominal: 200, tanggal: "2024-12-21", kategori: "good" },
    { nominal: 200, tanggal: "2024-12-21", kategori: "good" },
    { nominal: 200, tanggal: "2024-12-21", kategori: "good" },
    { nominal: 200, tanggal: "2024-12-21", kategori: "good" },
    { nominal: 200, tanggal: "2024-12-21", kategori: "good" },
    { nominal: 200, tanggal: "2024-12-21", kategori: "good" },
    { nominal: 200, tanggal: "2024-12-21", kategori: "good" },
    { nominal: 200, tanggal: "2024-12-21", kategori: "good" },
    { nominal: 200, tanggal: "2024-12-21", kategori: "good" },
    { nominal: 200, tanggal: "2024-12-21", kategori: "good" },
    { nominal: 200, tanggal: "2024-12-21", kategori: "good" },
    { nominal: 200, tanggal: "2024-12-21", kategori: "good" },
    { nominal: 200, tanggal: "2024-12-21", kategori: "good" },
    { nominal: 200, tanggal: "2024-12-21", kategori: "good" },
    { nominal: 200, tanggal: "2024-12-21", kategori: "good" },
    { nominal: 200, tanggal: "2024-12-21", kategori: "good" },
    { nominal: 200, tanggal: "2024-12-21", kategori: "good" },
    { nominal: 200, tanggal: "2024-12-21", kategori: "good" },
    { nominal: 200, tanggal: "2024-12-21", kategori: "good" },
    { nominal: 200, tanggal: "2024-12-21", kategori: "good" },
    { nominal: 200, tanggal: "2024-12-21", kategori: "good" },
    { nominal: 200, tanggal: "2024-12-21", kategori: "good" },
    { nominal: 200, tanggal: "2024-12-21", kategori: "good" },
    { nominal: 200, tanggal: "2024-12-21", kategori: "good" },
    { nominal: 200, tanggal: "2024-12-21", kategori: "good" },
    { nominal: 200, tanggal: "2024-12-21", kategori: "good" },
    { nominal: 200, tanggal: "2024-12-21", kategori: "good" },
    { nominal: 200, tanggal: "2024-12-21", kategori: "good" },
    { nominal: 200, tanggal: "2024-12-21", kategori: "good" },
    { nominal: 200, tanggal: "2024-12-21", kategori: "good" },
    { nominal: 200, tanggal: "2024-12-21", kategori: "good" },
    { nominal: 200, tanggal: "2024-12-21", kategori: "good" },
    { nominal: 200, tanggal: "2024-12-21", kategori: "good" },
    { nominal: 200, tanggal: "2024-12-21", kategori: "good" },
    { nominal: 200, tanggal: "2024-12-21", kategori: "good" },
    { nominal: 200, tanggal: "2024-12-21", kategori: "good" },
    { nominal: 200, tanggal: "2024-12-21", kategori: "good" },
    { nominal: 200, tanggal: "2024-12-21", kategori: "good" },
    { nominal: 200, tanggal: "2024-12-21", kategori: "good" },
  ];

  transactions.forEach((transaction) => {
    let clone = template.content.cloneNode(true);

    let nominalP = clone.querySelector("#nominal");
    let tanggalP = clone.querySelector("#tanggal");
    let kategoriP = clone.querySelector("#kategori");

    nominalP.innerHTML = transaction.nominal;
    tanggalP.innerHTML = transaction.tanggal;
    kategoriP.innerHTML = transaction.kategori;

    scrollContainer.appendChild(clone);
  });
}

async function fetchTransactions() {
  let response = await fetch(transactionEndpoint);
  let transactionList = response.json();
  return transactionList;
}

window.onload = () => {
  renderTransactions();
};
