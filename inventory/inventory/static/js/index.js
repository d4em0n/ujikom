import './bulma.js'
import $ from 'jquery'

$("#action-pinjam").click(function (e){
    var n = $("input:checked").length
    if (n <= 0) {
        alert("Anda belum memilih data apapun");
        return;
    }
    alert("Data akan segera dipinjam");
})

$("#data-barang-check-all").click(function (e) {
    $('td input:checkbox').prop('checked', this.checked);
})

function hello() {
    console.log("Hello world");
}

hello();