const modal = document.getElementById("transaction-modal");
const date = modal.querySelector("#date");
const form = modal.querySelector("#input-form");
const topupTemplate = form.querySelector("#topup-template");
const payTemplate = form.querySelector("#pay-template");
const transferTemplate = form.querySelector("#transfer-template");
const withdrawTemplate = form.querySelector("#withdraw-template");
const csrfToken = document.querySelector("[name=csrfmiddlewaretoken]");

let jasaDropdown;

let formMode = "topup";
let currentTemplate;

const templates = new Map([
  ["topup", [topupTemplate, "topup/"]],
  ["pay", [payTemplate, "payment/"]],
  ["transfer", [transferTemplate, "transfer/"]],
  ["withdraw", [withdrawTemplate, "withdraw/"]],
]);

function handleTypeChange(e) {
  formMode = e.target.value;
  csrfCopy = csrfToken.cloneNode(true);

  if (formMode === "pay") {
    renderBills();
  } else if (formMode === "withdraw") {
    renderBanks();
  }

  currentTemplate = templates.get(formMode)[0];
  form.replaceChildren(currentTemplate.content.cloneNode(true));
  form.appendChild(csrfCopy);
}

async function fetchBills() {
  let response;
  try {
    response = await fetch("fetch_bills/");
    if (!response.ok) {
      throw new Error("Failed to fetch bills");
    }

    return await response.json();
  } catch (error) {
    console.error(error);
    return;
  }
}

async function renderBanks() {
  let response;
  try {
    response = await fetch("fetch_banks/");
    if (!response.ok) {
      throw new Error("Failed to fetch banks");
    }

    response = await response.json();
  } catch (error) {
    console.error(error);
    return;
  }

  const banks = response.data;

  const bankDropdown = form.querySelector("#bank-dropdown");

  banks.forEach((bank) => {
    const option = document.createElement("option");
    option.value = bank.id;
    option.textContent = bank.nama;
    bankDropdown.appendChild(option);
  });
}

async function renderBills() {
  bills = await fetchBills();

  jasaDropdown = form.querySelector("#jasa-dropdown");

  if (!bills) {
    const option = document.createElement("option");
    option.value = "";
    option.textContent = "Tidak ada pemesanan yang menunggu pembayaran";
    option.disabled = true;
    jasaDropdown.appendChild(option);
    return;
  }

  bills.data.forEach((bill) => {
    const option = document.createElement("option");
    option.value = bill.id;
    option.textContent =
      bill.subkategori + " | Sesi " + bill.sesi + " - " + bill.totalbiaya;
    jasaDropdown.appendChild(option);
  });
}

async function handleFormSubmit(e) {
  e.preventDefault();
  const formData = new FormData(form);
  console.log(formData.entries());

  let response;
  const postData = {
    method: "POST",
    body: formData,
  };

  try {
    response = await fetch(templates.get(formMode)[1], postData);
    if (!response.ok) {
      throw new Error("Failed to submit form");
    }
  } catch (error) {
    console.error(error);
    return;
  }
}

// Set default to the topup form
form.appendChild(templates.get(formMode)[0].content.cloneNode(true));
form.reset();

const currentDate = new Date().toLocaleDateString();
date.textContent = currentDate;
