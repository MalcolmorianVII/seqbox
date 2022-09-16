const todo_btn = document.querySelector('.todo')
todo_btn.addEventListener('click',getTodo)

// const seq_data_btn = document.querySelector('.seqdata')
// seq_data_btn.addEventListener('click',processSeqData)

var xhr = null 

getXmlHttpRequestObject = function() {
    if (!xhr) {
        xhr = new XMLHttpRequest();
    }
    return xhr;
}

// function dataCallback() {
//     // Check if response is ready or not
//     if (xhr.readyState == 4 && xhr.status == 201) {
//         console.log("Get todo process initiated")

//     }
// }

function getTodo() {
    console.log('I can get todo!!')
    // Alert backend to start the get_todolist process
    const ALERTCODE = 1

    xhr = getXmlHttpRequestObject()

    // xhr.onreadystatechange = dataCallback()
    //async request
    xhr.open("POST","http://127.0.0.1:5000/get_todolist",true)
    xhr.setRequestHeader("Content-Type","text;charset=UTF-8")
    //send the request over the network
    xhr.send(ALERTCODE)
}
