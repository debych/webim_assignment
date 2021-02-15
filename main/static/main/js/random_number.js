let token = $('input')[0].value

function update_random_number(){
    $.ajax({url: '/main/get_rnd_number', dataType: "json", headers: { "X-CSRFToken": token }, type: 'POST'}).done(function (data){
        $('#random_number').text(data.number)
    })
}

setInterval(update_random_number, 5000)