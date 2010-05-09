$(document).ready(function(){ 
    tinyMCE.init({
        mode : "textareas",
        theme : "advanced",
        plugins: "table",
        theme_advanced_buttons1 : "bold,italic,underline,separator,strikethrough,justifyleft,justifycenter,justifyright, justifyfull,bullist,numlist,undo,redo,link,unlink",
        theme_advanced_buttons2 : "tablecontrols,|,code",
        theme_advanced_buttons3 : "",
        theme_advanced_toolbar_location : "top",
        theme_advanced_toolbar_align : "left",
        theme_advanced_statusbar_location : "bottom",
    });
});


