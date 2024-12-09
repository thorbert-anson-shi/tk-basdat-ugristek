const scrollContainer = document.querySelector("#scroll-container");
const template = document.querySelector("#transaction-item");
const transactionModal = document.querySelector("#transaction-modal");
const transactionEndpoint = "/transactions/";

function handleCreateTransaction() {
  transactionModal.showModal();
}

async function fetchTransactions() {
  let response = await fetch("/mypay/fetch_transactions/");
  let transactionList = response.json();
  return transactionList;
}

async function renderTransactions() {
  // Empty table before each rerender
  scrollContainer.replaceChildren();

  const transactions = await fetchTransactions();

  transactions.data.forEach((transaction) => {
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

window.onload = () => {
  renderTransactions();
};
