const reg_form = document.getElementById("regForm");
const uname = document.getElementById("name");
const email = document.getElementById("email");
const passwd = document.getElementById("password");

document.addEventListener("submit", (e) => {
  e.preventDefault();

  fetch("/register", {
    method: "POST",
    headers: {
      "Content-Type": "Application/json",
    },
    body: JSON.stringify({
      name: uname.value,
      email: email.value,
      passwd: passwd.value,
    }),
  }).then((res) =>
    res.json().then((data) => {
      if (data.status == 201) {
        return window.location.replace("/login");
      }
      if (data.status == 400) {
        console.log(data.msg);
      }
    })
  );
});
