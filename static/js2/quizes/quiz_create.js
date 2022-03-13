$(document).ready(function(){


    $('#add_more_answer').click(function () {
        let total_answer = $('#id_answers-TOTAL_FORMS');
        let form_idx = total_answer.val();
    
        $('#formset_wrapper').append($('#emptyanswer_wrapper').html().replace(/__prefix__/g, form_idx));
        
        total_answer.val(parseInt(form_idx)+1);
    });
    
    $('#add_more_question').click(function () {
        let total_question = $('#id_questions-TOTAL_FORMS');
        let form_idx = total_question.val();
    
        $('#formset_wrapper').append($('#emptyquestion_wrapper').html().replace(/__prefix__/g, form_idx));
        
        total_question.val(parseInt(form_idx)+1);
    }); 
})
