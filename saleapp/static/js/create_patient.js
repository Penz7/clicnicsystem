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
    fetch('/patient/register', {
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
                alert("Đăng ký khám thành công")
            }
             if (data.status === 100){
                alert("Danh sách người dùng trong ngày đã kín!! Đợi đăng ký vào ngày hôm sau")
            }
            if (data.status === 500 ){
                alert("Hệ thống đang có lỗi!")
            }
    }) // promise
}