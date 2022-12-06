const zapatoForm = document.querySelector('#zapatoForm')

var token = localStorage.getItem('token');
let zapatos = []
let edit =false;
let zapatoid=null;
window.addEventListener('DOMContentLoaded',async () => {
    const response = await fetch('/zapatos',{
        method:'GET',
        headers:{
            'Content-Type': 'application/json',
            'token':token
        },
       
       })
    const data = await response.json()
    
    ventas = data
    console.log(ventas)
    renderUser(ventas)
    
});



function renderUser(zaps){
    
    const zapatoList = document.querySelector('#zapatoList')
    zapatoList.innerHTML = ''
    for (var i = 0; i < zaps.zapatos.length; i++) {
        for (const zapatos of Object.keys(zaps)) {
            // console.log(zaps.zapatos[0].nombre)
            const zapato = zaps.zapatos[0].nombre;
            const zapatoItem = document.createElement('li')
            zapatoItem.classList ='list-group-item list-group-item-dark my-2'
            zapatoItem.innerHTML = `
            <header class="d-flex justify-content-between align-items-center">
           
            <div>
            <button onclick="eliminar(${zaps.zapatos[i].id})" class="btn-delete btn btn-danger btn-sm"> borrar </button>
            <button onclick="actualizar(${zaps.zapatos[i].id})" class="btn-edit btn btn-secondary btn-sm"> Editar</button>
            </div>
            </header>
            <h3>Nombre:${zaps.zapatos[i].nombre}</h3>
            <h3>Modelo:${zaps.zapatos[i].modelo}</h3>
            <h3>Precio:${zaps.zapatos[i].precio}</h3>
            <h3>Talla:${zaps.zapatos[i].talla}</h3>
            `
         
            
         

            zapatoList.append(zapatoItem)
        }
        
      }
    
}


zapatoForm.addEventListener('submit', async e =>{
    e.preventDefault()
    
 
   const nombre =  zapatoForm['nombre'].value
   const modelo =  zapatoForm['modelo'].value
   const precio =  zapatoForm['precio'].value
   const talla =  zapatoForm['talla'].value
   if(!edit){   
   const response = await fetch('/auth/registrozapato',{
    method:'POST',
    headers:{
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({
        nombre,
        modelo,
        precio,
        talla
    })
   })
   const data = await response.json()
   }else{
    console.log('si')
    const response = await fetch(`/auth/actualizarzapato/${zapatoid}`,{
        method:'PUT',
        headers:{
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            nombre,
            modelo,
            precio,
            talla
        })
       })
       
       const data = await response.json()
       console.log(data)
   }
   
   
   zapatoForm.reset();
})


async function eliminar(id) {
    console.log(id)
    const response = await fetch(`/auth/eliminarzapato/${id}`,{
        method:'DELETE',
        headers:{
            'Content-Type': 'application/json'
        }
        
       })
       const data =  await response.json()
}

async function actualizar(id) {
    const response = await fetch(`/zapatos/${id}`,{
        method:'GET',
        
       })
    const data = await response.json()
    console.log(data)
  
    zapatoForm["nombre"].value = data.zapatos[0].nombre
    zapatoForm["modelo"].value = data.zapatos[0].modelo;
    zapatoForm["precio"].value = data.zapatos[0].precio;
    zapatoForm["talla"].value = data.zapatos[0].talla;
    edit = true;
    zapatoid = data.zapatos[0].id;
}