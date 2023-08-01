const username_field = document.getElementById("userName");

username_field.addEventListener("change", (e) => {
    let username = e.target.value;
    if(username.length > 0)
    {
        let body = { "username" : username };
        const options = {
            method: 'POST',
            headers: {'content-type': 'application/json'},
            body: JSON.stringify(body)
        };
        
        fetch('/authentication/validate-username', options)
        .then(response => response.json())
        .then(response => {
            let username_lable = document.getElementById("userNameLable");
            if(response["username_valid"])
            {
                username_lable.style.display = "none";
                username_lable.textContent = "Username available";
            }
            else if(response["username_error"])
            {
                username_lable.style.display = "block";
                username_lable.textContent = response["username_error"];
            }
        })
        .catch(err => console.error(err));
    }
});

const email_field = document.getElementById("inputEmail");

email_field.addEventListener("change", (e) => {
    let email = e.target.value;

    if(email.length > 0)
    {
        let body = {"email":email};
        let options = {
            method: "POST",
            headers: {"content-type":"application/json"},
            body: JSON.stringify(body)
        }

        fetch("/authentication/validate-email", options)
        .then(response => response.json())
        .then(response => {
            let email_lable = document.getElementById("emailLable")
            if(response["useremail_valid"])
            {
                email_lable.style.display = "none";
                email_lable.textContent = "Valid Email ID";
            }
            else if (response["useremail_error"])
            {
                email_lable.style.display = "block";
                email_lable.textContent = response["useremail_error"];
            }
        })
        .catch(error => console.log(error))
    }
});

const password = document.getElementById("inputPassword");
const repassword = document.getElementById("inputRePassword");

function check_password()
{
    let password_value = password.value;
    let repassword_value = repassword.value;
    if(password_value.length > 0 && repassword_value.length > 0)
    {
        let body = {
            'password': password_value,
            'repassword': repassword_value
        };
        let options = {
            method: "POST",
            headers: {"content-type":"application/json"},
            body: JSON.stringify(body)
        }
        fetch("/authentication/validate-password", options)
        .then(response => response.json())
        .then(response => {
            let password_lable = document.getElementById("passwordLable");
            if(response["userpassword_valid"])
            {
                password_lable.style.display = "none";
            }
            else if(response["userpassword_error"])
            {
                password_lable.style.display = "block";
                password_lable.textContent = response["userpassword_error"];
            }
        })
        .catch(err => console.log(err))
    }
}

password.addEventListener("change", check_password)
repassword.addEventListener("change", check_password)