// saat dokumen HTML sudah terload sempurna, function show_bucket() akan berjalan
$(document).ready(function () {
    show_bucket();
});
function show_bucket(){
    $('#bucket-list').empty();
    // menjalankan ajax request dengan type GET untuk mengambil data dari Object buckets pada json, yang sebelumnya sudah dikirimkan oleh server
    $.ajax({
        type: "GET",
        url: "/bucket",
        data: {},
        success: function (response) {
            let rows = response['buckets'];
            // perulangan yang di dalamnya dibuat variable untuk menampung list dari response object 'buckets'
            for (let i = 0; i < rows.length; i++) {
                let bucket = rows[i]['bucket'];
                let num = rows[i]['num'];
                let done = rows[i]['done'];
                let temp_html = '';

                // jika suatu data memiliki value 0 pada key 'done', akan memasukan struktur html yang memiliki tombol done
                if (done === 0) {
                    temp_html = `
                    <li>
    <h2>🔲 ${bucket}</h2>
    <button onclick="done_bucket(${num})" type="button" class="btn btn-outline-primary">Done!</button>
    <button onclick="delete_bucket(${num})" type="button" class="btn btn-outline-danger">Delete</button>
</li>`;
                } else {
                    // jika data pada key 'done' bukan 0, maka tombol done tidak akan ditampilkan
                    temp_html = `
                    <li>
    <h2 class='done'>✅ ${bucket}</h2>
    <button onclick="delete_bucket(${num})" type="button" class="btn btn-outline-danger
    ">Delete</button>
</li>`;
                }
                // function untuk melampirkan variable temp_html pada struktur html yang memiliki id=bucket-list
                $('#bucket-list').append(temp_html);
            }
        }
    });
}
function save_bucket(){
    // variable untuk menampung data yang diinput oleh user pada form yang memiliki id=bucket
    let bucket = $('#bucket').val();
    $.ajax({
        // menjalankan ajax dengan type POST untuk memasukkan data input user untuk dimasukkan ke dalam data key bucket_give yang nantinya akan diambil oleh server
        type: "POST",
        url: "/bucket",
        data: {bucket_give: bucket},
        success: function (response) {
            alert(response["msg"])
            window.location.reload();
        }
    });
}
function done_bucket(num){
    $.ajax({
        type: "POST",
        url: "/bucket/done",
        data: {num_give: num},
        success: function (response) {
            alert(response["msg"])
            window.location.reload();
        }
    });
}
function delete_bucket(num){
    $.ajax({
        type: "POST",
        url: "/delete",
        data: {num_give : num},
        success: function (response) {
            alert(response["msg"])
            window.location.reload();
        }
    });
}