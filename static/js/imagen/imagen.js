
const userForm = document.querySelector('#formImagen')

userForm.addEventListener('submit', async e =>{
    e.preventDefault()
    const formData = new FormData(event.target);
    let datos = {
        inputFile: formData,
      }
    console.log('hola')
   const response = await fetch('/uploadPerfil',{
    method:'POST',
    headers:{
        'Content-Type': 'multipart/form-data',
        'token':'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2NzAyMjQ4MTQsImlhdCI6MTY3MDEzODQxNCwic3ViIjoxfQ.wsAFGxO8Orv_U4moUE1eDeWuJwtN9PgjLyYuds2RBTY'
    },
    body: JSON.stringify({
        datos
    })
   })
   const data = await response.json()
   console.log(data)

})


// const handleSubmit = (event) => {
//     alert('hola')
//     event.preventDefault(); //Previene que se recargue la página al hacer submit.
//     console.log('hola')
//     const formData = new FormData(event.target); //event.target es el formulario
//     console.log(formData)
//     fetch('/uploadPerfil', {
//       method: "POST",
//       body: formData,
//       headers: { "Content-Type": "multipart/inputFile" },
//     });
//     console.log('salida')
//   };