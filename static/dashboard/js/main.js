const btnDelete = document.querySelectorAll('.delete')

if(btnDelete) {
    const btnArray = Array.from(btnDelete);
    btnArray.forEach((btn) =>{
        btn.addEventListener('click',(e) =>{
            if(!confirm('¿Estas seguro de eliminar este registro?')){
                e.preventDefault();
            }
        });
    });
}