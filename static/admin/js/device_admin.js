(function($) {
    $(document).ready(function() {
        function toggleFields() {
            var type = $('#id_device_type').val();
            if (type === 'computer') {
                $('.computer-fields').show();
                $('.console-fields').hide();
            } else if (type === 'console') {
                $('.computer-fields').hide();
                $('.console-fields').show();
            } else {
                $('.computer-fields').hide();
                $('.console-fields').hide();
            }
        }
        toggleFields();
        $('#id_device_type').change(toggleFields);
    });
})(django.jQuery);