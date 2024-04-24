const csrf = document.getElementsByName('csrfmiddlewaretoken')[0].value
console.log(csrf)
const alertBox = document.getElementById("alert-box")

const handleAlerts = (type, msg)=>{
    alertBox.innerHTML = `<div class="alert alert-${type}" role="alert">
    ${msg}
  </div>`
}


Dropzone.autoDiscover = false
const myDropzone = new Dropzone('#my-dropzone', {
    url: '/upload/',
    init: function(){
        this.on('sending', function(file, xhr, formData){
            console.log('sending')
            formData.append('csrfmiddlewaretoken', csrf)
        })
        this.on('success', function(file, response){
            console.log(response)
            const ex = response.success
            const message = response.message
            if(ex){
                handleAlerts('success', message)     
            }else{
                
                handleAlerts('danger', message)
            }
        })
    },
    maxFiles:3,
    maxFilesize:3,
    acceptedFiles:'.csv'
})



