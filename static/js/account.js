const ulogo = document.getElementById("ulogo");
const uname = document.getElementById("uname");
const uemail = document.getElementById("uemail");

const logout = document.getElementById("logout");

window.addEventListener("load", () => {
  atoken = localStorage.getItem("atoken");
  fetch("/jwt/user", {
    method: "GET",
    headers: { Authorization: "Bearer " + atoken },
  }).then((resp) =>
    resp.json().then((data) => {
      if (!data) {
        window.location.href = "/login";
      }
      ulogo.innerText = data.name[0];
      uname.innerText = data.name;
      uemail.innerText = data.email;
    })
  );
});

logout.addEventListener("click", () => {
  fetch("/jwt/logout", {
    method: "POST",
    headers: {
      Authorization: "Bearer " + localStorage.getItem("atoken"),
    },
  }).then((res) =>
    res.json().then((data) => {
      if (data) {
        localStorage.removeItem("atoken");
        window.location.href = "/login";
      }
    })
  );
});
