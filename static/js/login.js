const form = document.getElementById("loginForm");

const email = document.getElementById("email");
const passwd = document.getElementById("password");

document.addEventListener("submit", (e) => {
  e.preventDefault();

  fetch("/login", {
    method: "POST",
    headers: {
      "Content-Type": "Application/json",
    },
    body: JSON.stringify({ email: email.value, passwd: passwd.value }),
  }).then((res) =>
    res.json().then((data) => {
      console.log(data);
      localStorage.setItem("atoken", data.access_token);
      window.location.href = "/";
    })
  );
});
