const ventaForm = document.querySelector('#ventaForm')

var token = localStorage.getItem('token');
let ventas = []
let edit =false;
let ventaid=null;

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

