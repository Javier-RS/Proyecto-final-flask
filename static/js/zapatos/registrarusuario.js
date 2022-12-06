const userForm = document.querySelector('#userForm')

userForm.addEventListener('submit', async e =>{
    e.preventDefault()
    
   
   const password =  userForm['password'].value
   const email =  userForm['email'].value
    
   const response = await fetch('/auth/registro',{
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
   
   userForm.reset();
})
