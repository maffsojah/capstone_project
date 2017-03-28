$(document).ready(function() {
    var table = $('#customers').DataTable({
        columnDefs: [{
            targets: [0],
            searchable: false,
            orderable: false,
            className: 'mdl-data-table__cell--non-numeric',
            render: function(data, type, full, meta) {
                return '<input type="checkbox" name="id[]" value="' + $('<div/>').text(data).html() + '">';
            }
        }],
        'order': [1, 'asc']
    });
    // Handle click on "Select all" control
    $('#example-select-all').on('click', function() {
        // Get all rows with search applied
        var rows = table.rows({
            'search': 'applied'
        }).nodes();
        // Check/uncheck checkboxes for all rows in the table
        $('input[type="checkbox"]', rows).prop('checked', this.checked);
    });

    // Handle click on checkbox to set state of "Select all" control
    $('#customers tbody').on('change', 'input[type="checkbox"]', function() {
        // If checkbox is not checked
        if (!this.checked) {
            var el = $('#example-select-all').get(0);
            // If "Select all" control is checked and has 'indeterminate' property
            if (el && el.checked && ('indeterminate' in el)) {
                // Set visual state of "Select all" control
                // as 'indeterminate'
                el.indeterminate = true;
            }
        }
    });

    // Handle form submission event
    $('#frm-example').on('submit', function(e) {
        var form = this;

        // Iterate over all checkboxes in the table
        table.$('input[type="checkbox"]').each(function() {
            // If checkbox doesn't exist in DOM
            if (!$.contains(document, this)) {
                // If checkbox is checked
                if (this.checked) {
                    // Create a hidden element
                    $(form).append(
                        $('<input>')
                        .attr('type', 'hidden')
                        .attr('name', this.name)
                        .val(this.value)
                    );
                }
            }
        });
        // FOR TESTING ONLY

        // Output form data to a console
        $('#example-console').text($(form).serialize());
        console.log("Form submission", $(form).serialize());

        // Prevent actual form submission
        e.preventDefault();
    });
});
