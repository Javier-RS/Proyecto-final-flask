window.addEventListener('DOMContentLoaded', () => {
   var userID = localStorage.getItem('token');
    if(userID == 'undefined' || userID == null){
        window.location.href = "/login";
    }
});
