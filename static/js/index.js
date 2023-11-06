window.addEventListener("load", () => {
  atoken = localStorage.getItem("atoken");
  fetch("/jwt/verify", {
    method: "GET",
    headers: { Authorization: "Bearer " + atoken },
  }).then((resp) =>
    resp.json().then((data) => {
      if (!data) {
        window.location.href = "/login";
      }
    })
  );
});
