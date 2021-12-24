const form = document.querySelector("form");
form.onsubmit = (e) => {
  e.preventDefault();
  const token = document.getElementsByName("csrfmiddlewaretoken")[0].value;
  const item = document.getElementsByName("item")[0].value;
  fetch("/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": token,
    },
    body: JSON.stringify({
      item: item,
    }),
  }).then((response) => {
    if (response.ok) {
      window.location.reload();
    } else {
      alert("Error: " + response.statusText);
      window.location.reload();
    }
  });
};

const buyButtons = document.querySelectorAll(".buyButton");
buyButtons.forEach(
  (button) =>
    (button.onclick = (e) => {
      makeRequest(e.target, `/purchase/${button.value}/`, "PUT");
    })
);

const deleteButtons = document.querySelectorAll(".deleteButton");
deleteButtons.forEach(
  (button) =>
    (button.onclick = (e) =>
      makeRequest(e.target, `/delete/${button.value}/`, "DELETE"))
);

const restoreButton = document.querySelectorAll(".restoreButton");
restoreButton.forEach(
  (button) =>
    (button.onclick = (e) =>
      makeRequest(e.target, `/restore/${button.value}/`, "PUT"))
);

function makeRequest(element, url, method) {
  const token = document.getElementsByName("csrfmiddlewaretoken")[0].value;
  fetch(url, {
    method: method,
    headers: {
      "X-CSRFToken": token,
    },
  })
    .then((response) => {
      console.log(response);
      if (response.ok) {
        window.location.reload();
      } else {
        alert("Error: " + response.statusText);
        window.location.reload();
      }
      if (method === "PUT") {
        const purchasedList = document.getElementById("purchasedList");
      }
    })
    .catch((error) => {
      window.location.reload();
    });
}