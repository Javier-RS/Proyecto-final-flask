const ventaForm = document.querySelector('#ventaForm')

var token = localStorage.getItem('token');
let ventas = []
let edit =false;
let ventaid=null;
window.addEventListener('DOMContentLoaded',async () => {
    const response = await fetch('/ventas',{
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
    console.log(zaps)
    const ventaList = document.querySelector('#ventaList')
    ventaList.innerHTML = ''
    for (var i = 0; i < zaps.ventas.length; i++) {
        for (const ventas of Object.keys(zaps)) {
            // console.log(zaps.zapatos[0].nombre)
            const zapato = zaps.ventas[0].referencia;
            const ventaItem = document.createElement('li')
            ventaItem.classList ='list-group-item list-group-item-dark my-2'
            ventaItem.innerHTML = `
            <header class="d-flex justify-content-between align-items-center">
           
            <div>
            <button onclick="eliminar(${zaps.ventas[i].id})" class="btn-delete btn btn-danger btn-sm"> borrar </button>
            <button onclick="actualizar(${zaps.ventas[i].id})" class="btn-edit btn btn-secondary btn-sm"> Editar</button>
            </div>
            </header>
            <h3>Nombre:${zaps.ventas[i].referencia}</h3>
            <h3>Modelo:${zaps.ventas[i].cantidad}</h3>
            `
         
            
         

            ventaList.append(ventaItem)
        }
        
      }
    
}


ventaForm.addEventListener('submit', async e =>{
    e.preventDefault()
    
 
   const referencia =  ventaForm['referencia'].value
   const cantidad =  ventaForm['cantidad'].value
   if(!edit){   
   const response = await fetch('/auth/registroventa',{
    method:'POST',
    headers:{
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({
        referencia,
        cantidad
     
    })
   })
   const data = await response.json()
   }else{
    console.log('si')
    const response = await fetch(`/auth/actualizarventa/${ventaid}`,{
        method:'PUT',
        headers:{
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
           referencia,
           cantidad
        })
       })
       
       const data = await response.json()
       console.log("========")
       console.log(data)
   }
   
   
   ventaForm.reset();
})


async function eliminar(id) {
    console.log(id)
    const response = await fetch(`/auth/eliminarventa/${id}`,{
        method:'DELETE',
        headers:{
            'Content-Type': 'application/json'
        }
        
       })
       const data =  await response.json()
}

async function actualizar(id) {
    const response = await fetch(`/ventas/${id}`,{
        method:'GET',
        
       })
    const data = await response.json()
    console.log("------")
    console.log(data)
  
    ventaForm["referencia"].value = data.ventas[0].referencia
    ventaForm["cantidad"].value = data.ventas[0].cantidad;
    
    edit = true;
 
    ventaid = data.ventas[0].id;
    
}