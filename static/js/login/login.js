const userForm = document.querySelector('#formSubmitLogin')

userForm.addEventListener('submit', async e =>{
    e.preventDefault()
    
   
   const password =  userForm['password'].value
   const email =  userForm['email'].value
   const response = await fetch('/auth/login',{
    method:'POST',
    headers:{
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({
        email,
        password
    })
   })
   const data = await response.json()
   
   token = data.auth_token
   localStorage.setItem('token', token);
   if(token != undefined){
    alert('Bienvenido')
    window.location.href = "/home";
   }
   else{}
   
})