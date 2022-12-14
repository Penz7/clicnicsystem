
function saveMedicineExaminationBill() {
     medicine_price_total_pay = document.getElementById('medicine_price_total_pay').innerHTML
     total_price_pay = document.getElementById('total_price_pay').innerHTML
     medical_examination_id = document.getElementById('medical_examination_id').value
     medical_examination_price_pay = document.getElementById('medical_examination_price_pay').value
     account_id_current = document.getElementById('account_id_current').innerHTML
    fetch('/api/cashier/save_medical_examination_bill', {
        method: 'post',
        body: JSON.stringify({
                'medical_price': medicine_price_total_pay,
                'total_price': total_price_pay,
                'medical_examination_id': medical_examination_id,
                'account_id_current':account_id_current,
                'medical_examination_price_pay' :medical_examination_price_pay,
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(res => res.json()).then((data) => {
        console.info(data)
            if (data.status === 204){
                alert("Thanh toán thành công")
            }
            else{
                alert("Hệ thống đang có lỗi!")
            }
    }) // promise
}


function loadPatient() {
    order_id = $('#medicine_list_datas').children().length + 1
    patient_fullname_pay = document.getElementById('patient_fullname_pay')
    patient_card_id_pay = document.getElementById('patient_card_id_pay')
    medical_examination_id_pay = document.getElementById('medical_examination_id_pay')
    medical_examination_date_created = document.getElementById('medical_examination_date_created')
    predicted_disease_patient = document.getElementById('predicted_disease_patient')
    medicine_price_total_pay = document.getElementById('medicine_price_total_pay')
    medical_examination_price_pay = document.getElementById('medical_examination_price_pay')
    total_price_pay = document.getElementById('total_price_pay')


    medical_examination_id = document.getElementById('medical_examination_id').value
    fetch('/api/pay/load_patient_info', {
    method: 'post',
        body: JSON.stringify({
                'medical_examination_id': medical_examination_id
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(res => res.json()).then(data => {
      console.log(medical_examination_id)
      console.log(data)
      if (data.status === 500){
                alert("Không tìm thấy phiếu khám")
      }
      else{
        data_patient = data[0]
        medicine_patient = data[1]
        total_price = data[2]
        console.info(data[0])
        console.info(total_price)

         data_patient.forEach(c => {
                patient_fullname_pay.innerHTML = `${c.last_name_patient} ${c.first_name_patient}`
                patient_card_id_pay.innerHTML = `${c.id_card_patient}`
                medical_examination_id_pay.innerHTML =`${c.medical_examination_id}`
                medical_examination_date_created.innerHTML =`${c.data_created}`
                predicted_disease_patient.innerHTML =`${c.predicted_disease}`
                })
        let h = ''
        medicine_patient.forEach(c => {
            h += `<tr>
                <td>${order_id}</td>
                <td>${c.medicine_name} </td>
                <td>${c.medicine_unit}</td>
                <td>${c.medicine_amount}</td>
                <td>${c.medicine_price}</td>
                <td>${c.total}</td>
                </tr>`
        })
        let list_medicine = document.getElementById('medicine_list_datas')
        list_medicine.innerHTML = h
        medicine_price_total_pay.innerHTML = total_price
        m = parseInt(total_price_pay.innerHTML)
        j = parseInt(medical_examination_price_pay.value)
        k = parseInt(medicine_price_total_pay.innerHTML)
        m = j + k;
        total_price_pay.innerHTML = m
}
})
}
