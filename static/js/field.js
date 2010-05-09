
$(document).ready(function(){
    $('#id_field_type').change(type_selected);
    type_selected();
});

function type_selected(){
    val = $('#id_field_type').val();
    if(val == "textarea"){
        $('#id_row_rows').show(); 
        $('#id_row_cols').show(); 
        $('#id_row_max_length').hide();
    }
    else if(val == "dropdown" || val == "dropdownmul" || val == "checkbox" || val == "radio"){
        $('#id_row_choices').show();
        $('#id_row_max_length').hide();
    }
    else{
        $('#id_row_rows').hide(); 
        $('#id_row_cols').hide(); 
        $('#id_row_choices').hide();
        $('#id_row_max_length').show();
    }
}
