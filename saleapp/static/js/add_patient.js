function checkPatient() {
    let id_card_input = document.getElementById("id_card_input").value
    let last_name = document.getElementById("last_name").value
    let first_name = document.getElementById('first_name').value
    let email = document.getElementById('email').value
    let phone_number = document.getElementById('phone_number').value
        if (id_card_input == null || id_card_input.length <= 0) {
            alert('Thông tin bệnh nhân không được để trống')
            return
        }
        if (last_name == null || last_name.length <= 0) {
             alert('Thông tin họ không được để trống')
            return
        }
        if (first_name == null || first_name.length <= 0) {
            alert('Thông tin tên không được để trống')
            return
        }
        if (email == null || email.length <= 0) {
            alert('Thông tin email không được để trống')
            return
        }
          if (phone_number == null || phone_number.length <= 0) {
            alert('Thông tin điện thoại không được để trống')
            return
            }
        //save
        addPatient()
    }

function addPatient() {
    id_card_input = document.getElementById("id_card_input").value
    last_name = document.getElementById("last_name").value
    first_name = document.getElementById('first_name').value
    email = document.getElementById('email').value
    phone_number = document.getElementById('phone_number').value
    fetch('/api/nurse/add_patient', {
        method: 'post',
        body: JSON.stringify({
                'id_card_input': id_card_input,
                'last_name': last_name,
                'first_name': first_name,
                'email': email,
                'phone_number': phone_number
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(res => res.json()).then((data) => {
        console.info(data)
            if (data.status === 204){
                alert("Thêm bệnh nhân thành công")
            }
            else{
                alert("Hệ thống đang có lỗi!")
            }
    }) // promise
}

function loadPatient() {
    let id_patient_count = document.getElementById('id_patient_count')
    var order_id = $('#patient_datas').children().length + 1
    fetch('/api/nurse/patient').then(res => res.json()).then((data) => {
    console.info(data)
    let h = ""
    let id = 1
    data.forEach(c => {
            h += `<tr>
                     <td>
                       ${c.date_create}
                  </td>
                     <td>${id++}</td>
                     <td> ${c.last_name } ${ c.first_name }</td>
                     <td>${c.id_card}</td>
                     <td>${c.email}</td>
                     <td>${c.phone_number}</td>
                 </tr>`

    })
    let d = document.getElementById('patient_datas')
    a = 0
    u = a + id - 1
    d.innerHTML = h
    id_patient_count.innerHTML = u
})
}

