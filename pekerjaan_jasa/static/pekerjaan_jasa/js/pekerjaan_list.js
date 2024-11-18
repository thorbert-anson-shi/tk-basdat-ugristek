const statusDropdown = document.querySelector("#status-dropdown");

async function handleSearch() {
  let status = statusDropdown.value;
  let response = await fetch(
    "/pekerjaan_jasa/?" + new URLSearchParams({ status: status })
  );
}
