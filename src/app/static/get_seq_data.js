const get_seq_data_btn = document.querySelector('.getseq')
get_seq_data_btn.addEventListener('click',getSeqData)

var xhr = null 

getXmlHttpRequestObject = function() {
    if (!xhr) {
        xhr = new XMLHttpRequest();
    }
    return xhr;
}

function getSeqData() {
    // Alert backend to start the get_todolist process
    const ALERTCODE = 1

    xhr = getXmlHttpRequestObject()

    // xhr.onreadystatechange = dataCallback()
    //async request
    xhr.open("POST","http://127.0.0.1:5000/get_seq_data",true)
    xhr.setRequestHeader("Content-Type","text;charset=UTF-8")
    //send the request over the network
    xhr.send(ALERTCODE)
}