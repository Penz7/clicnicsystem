function addMedicine() {

    var order_id = $('#medicine_datas').children().length + 1
    var nameMedicine = $('#medicine_name_input').val()
    for (let i = 1; i <= $('#medicine_datas').children().length; i++)
        if (nameMedicine == $(`#medicine_datas tr:nth-child(${i}) td:nth-child(3)`).text().trim()) {
           alert( 'Tên thuốc đã tồn tại')
            return
        }

    var amountMedicine = $('#medicine_amount').val()
    var dosage = $('#dosage').val()
    var usingMethod = $('#using_method').val()

    var row = `<tr>
        <td> 
        <i class="far fa-trash-alt" onclick = "removeMedicine(${order_id})"></i>
        </td>
        <td>${order_id}</td>
        <td>${nameMedicine} </td>
        <td><span>${amountMedicine}</span></td>
        <td>${dosage}</td>
        <td>${usingMethod}</td>
        </tr>`
    $('#medicine_datas').append(row)
    $('#add_medicine_modal').modal('toggle')

}

function removeMedicine(order_id) {
    $(`#medicine_datas tr:nth-child(${order_id})`).remove()
    for (let i = 1; i <= $('#medicine_datas').children().length; i++)
        $(`#medicine_datas tr:nth-child(${i}) td:nth-child(2)`).text(i)
}

function checkMedicineName() {
        var medicineName = $('#medicine_name_input').val()
        var dosage = $('#dosage').val()
        var usingMethod = $('#using_method').val()
        var medical_examination_detail_id = $('#medical_examination_detail_id')
        if (medicineName == null || medicineName.length <= 0) {
            alert('Thông tin thuốc không được để trống')
            return
        }
        if (dosage == null || dosage.length <= 0) {
            alert('Thông tin liều dùng không được để trống')
            return
        }
        if (usingMethod == null || usingMethod.length <= 0) {
             alert('Thông tin phương pháp không được để trống')
            return
        }
         if (medical_examination_detail_id == null || medical_examination_detail_id.length <= 0) {
             alert('Mã phiếu khám không được để trống')
            return
        }
        addMedicine()
    }


function checkCustomerIdCard() {
        var idCard = $('#id_card_input').val()
        var symptom = $('#symptom').val()
        var predictedDisease = $('#predicted_disease').val()
        var medical_examination_id = $('#medical_examination_id').val()
        if (idCard == null || idCard.length <= 0) {
            alert('Thông tin bệnh nhân không được để trống')
            return
        }
        if (symptom == null || symptom.length <= 0) {
             alert('Thông tin triệu chứng không được để trống')
            return
        }
        if (predictedDisease == null || predictedDisease.length <= 0) {
            alert('Thông tin chuẩn đoán không được để trống')
            return
        }
        if (medical_examination_id == null || medical_examination_id.length <= 0) {
            alert('Mã phiếu khám không được để trống')
            return
        }
        //save
        saveMedicineExamination()
    }



function clearData() {
    $('#id_card_input').val('')
    $('#symptom').val('')
    $('#predicted_disease').val('')
    $('#medicine_datas').html('')
}

function saveMedicineExamination() {
    symptom = document.getElementById("symptom").value
    patient_id_card = document.getElementById("id_card_input").value
    predicted_disease = document.getElementById('predicted_disease').value
    medical_examination_id = document.getElementById('medical_examination_id').value
    fetch('/api/doctor/save_medical_examination_data', {
        method: 'post',
        body: JSON.stringify({
                'symptom': symptom,
                'predicted_disease': predicted_disease,
                'patient_id_card': patient_id_card,
                'medical_examination_id': medical_examination_id
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(res => res.json()).then((data) => {
        console.info(data)
            if (data.status === 204){
                alert("Thêm phiếu khám thành công")
            }
            else{
                alert("Hệ thống đang có lỗi!")
            }
    }) // promise
}

function saveMedicineExaminationDetail() {
    var order_id = $('#medicine_datas').children().length
    if (order_id != 0) {
        var medicine_list = []
        for (let i = 1; i <= $('#medicine_datas').children().length; i++)
            medicine_list.push({
                'medicine_name_id':  $(`#medicine_datas tr:nth-child(${i}) td:nth-child(3)`).text().trim(),
                'amount': $(`#medicine_datas tr:nth-child(${i}) td:nth-child(4) span`).text().trim(),
                'dosage': $(`#medicine_datas tr:nth-child(${i}) td:nth-child(5)`).text().trim(),
                'using_method': $(`#medicine_datas tr:nth-child(${i}) td:nth-child(6)`).text().trim()
            })

        var medical_examination_detail_id = document.getElementById('medical_examination_detail_id').value
        fetch('/api/doctor/save_medical_examination_detail_data', {
            method: 'post',
            body: JSON.stringify({
                    'medicine_list': medicine_list,
                    'medical_examination_detail_id': medical_examination_detail_id
            }),
            headers: {
                'Content-Type': 'application/json'
            }
        }).then(res => res.json()).then((data) => {
            console.log(medicine_list)
            console.log(medical_examination_detail_id)
            console.info(data)
                if (data.status === 204){
                    alert("Thêm thuốc vào phiếu thành công")
                }
                else{
                    alert("Hệ thống đang có lỗi!")
                }
        }) // promise
    } else {
        alert('Danh sách thuốc trống')
    }
}

