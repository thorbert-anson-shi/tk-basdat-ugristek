const modal = document.getElementById("transaction-modal");
const form = modal.querySelector("#input-form");
const topupTemplate = form.querySelector("#topup-template");
const payTemplate = form.querySelector("#pay-template");
const transferTemplate = form.querySelector("#transfer-template");
const withdrawTemplate = form.querySelector("#withdraw-template");

function handleTypeChange(e) {
  const template = templates.get(e.target.value);
  form.replaceChildren(template.content.cloneNode(true));
}

let templates = new Map([
  ["topup", topupTemplate],
  ["pay", payTemplate],
  ["transfer", transferTemplate],
  ["withdraw", withdrawTemplate],
]);

// Set default to the topup form
form.appendChild(topupTemplate.content.cloneNode(true));
