const userForm = document.querySelector('#userForm')

var token = localStorage.getItem('token');
let users = []
let edit =false;
let userid=null;
window.addEventListener('DOMContentLoaded',async () => {
    const response = await fetch('/usuarios',{
        method:'GET',
        headers:{
            'Content-Type': 'application/json',
            'token':token
        },
       
       })
    const data = await response.json()
    
    users = data
    
    renderUser(users)
    
});



function renderUser(users){
 
    const userList = document.querySelector('#userList')
    userList.innerHTML = ''
    for (var i = 0; i < users.usuarios.length; i++) {
        for (const usuarios of Object.keys(users)) {
            
            const user = users.usuarios[i].email;
            const userItem = document.createElement('li')
            userItem.classList ='list-group-item list-group-item-dark my-2'
            userItem.innerHTML = `
            <header class="d-flex justify-content-between align-items-center">
            <h3>Email:${users.usuarios[i].email}</h3>
           
            <div>
            <button onclick="eliminar(${users.usuarios[i].id})" class="btn-delete btn btn-danger btn-sm"> borrar </button>
            <button onclick="actualizar(${users.usuarios[i].id})" class="btn-edit btn btn-secondary btn-sm"> Editar</button>
            </div>
            </header>
            <p>Administrador:${users.usuarios[i].admin}</p>
            `
         
            
         

            userList.append(userItem)
        }
        
      }
    
}


userForm.addEventListener('submit', async e =>{
    e.preventDefault()
    
 
    const password =  userForm['password'].value
   const email =  userForm['email'].value
   if(!edit){   
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
   }else{
    const response = await fetch(`/auth/actualizar/${userid}`,{
        method:'PUT',
        headers:{
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            email,
            password
        })
       })
       const data = await response.json()
   }
   
   
   userForm.reset();
})


async function eliminar(id) {
    console.log(id)
    const response = await fetch(`/auth/eliminar/${id}`,{
        method:'DELETE',
        headers:{
            'Content-Type': 'application/json'
        }
        
       })
       const data =  await response.json()
}

async function actualizar(id) {
    console.log(id)
    console.log("_________________")
    const response = await fetch(`/usuarios/${id}`,{
        method:'GET',
        
       })
    const data = await response.json()
    console.log(data)

    userForm["email"].value = data.usuarios[0].email;
    edit = true;
    userid = data.usuarios[0].id;
}