$(document).ready( function () {
    $('#customers_table').DataTable( {
        responsive: true,
        dom: 'Bfrtip',
        buttons: [
            'copy', 'excel', 'pdf', 'csv'
        ]
    } );
} );