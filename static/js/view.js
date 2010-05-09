$(document).ready(function(){
        $('#id_fields').change(field_selected);
        $('#id_personas').change(persona_selected);
});

Array.prototype.has = function(value) {
    for (var i = 0;i < this.length; i++) {
        if (this[i] == value) {   return true; }
    }
    return false;
};

var view = new View();

View.prototype.toString = function(){
        str = "";
        for(var field in view.fal){
           str += field;
        }
        return str;
};

function load_fal(data){
    data = eval("("+data+")");
    view.fal = data['fal'];
    field_map = data['field_map'];
    persona_map = data['persona_map'];
    personas_added = new Array();
    for(fid in view.fal){ 
        add_field(fid,field_map[fid]);
        for(pid in view.fal[fid]){
            ele = $('#'+fid+'_perms');
            view.persona_perms[pid] = view.fal[fid][pid]
            add_permission(fid,ele,pid,persona_map[pid]);
            if(!personas_added.has(pid)){
                add_persona(pid,persona_map[pid]);
                personas_added.push(pid);
                $('#'+pid+'_perm').val(view.fal[fid][pid]);
                $('#id_personas').selectOptions(pid);
            }
        }
    }
}

function get_fal(view_id){
    $.ajax({url:'/view/'+view_id+'/get_fal/',type:'get',data:{},success:load_fal});
}

function add_field(id,label){
         $('#sel_fields').append(
            $('<p id="id_sel_'+id+'"><input type="checkbox" name="sel_fields" value="'+id+'" checked />'+label+' <table id="'+id+'_perms"></table> </p>')
         );
}

function add_persona(id,name){
        $('#sel_personas').append(
            $('<p id="id_sel_'+id+'">'+name+'<select onchange="update_persona_perm(\''+id+'\')" id="'+id+'_perm" >'+view.perm_options+'</select></p>')
        );
}

function update_field_perm(fid,pid){
        view.fal[fid][pid] = $('#fperm_'+fid).val();
}

function add_permission(fid,ele,id,name){
        view.fal[fid][id] = view.persona_perms[id];
        $(ele).append(
            $('<tr id="frow_'+fid+'" ><td>'+name+'</td><td><select name="fperm_'+fid+'_'+id+'" id="fperm_'+fid+'" onchange="update_field_perm(\''+fid+'\',\''+id+'\')'+'" >'+view.perm_options+'</select></td><td><a href="javascript://" onclick="javascript:$(\'#frow_'+fid+'\').remove();" ><img src="/site_media/images/delete.png" alt="Delete" border=0 /></a></td></tr>')
        );
        $('#fperm_'+fid).val(view.persona_perms[id]);
}

function field_selected(){
    $('#sel_fields').html("");
    $('#id_fields :selected').each(function(i,s){
            add_field($(s).val(),$(s).text());
    });
}

function persona_selected(){
    $('#sel_personas').html("");
    view.persona_perms = {};
    $('#id_personas :selected').each(function(i,s){
        view.persona_perms[$(s).val()] = 'rw';
        add_persona($(s).val(),$(s).text());
    });
}

function apply_permissions(){
    if($('#id_fields :selected').length < 1){
        alert('No Fields selected');
        return false;
    }
    if($('#id_personas :selected').length < 1){
        alert('No Personas selected');
        return false;
    }
    $('#id_fields :selected').each(function(i,selected){
        ele = $('#'+$(selected).val()+'_perms');
        $(ele).find('tr').remove();
        var fid = $(selected).val();
        view.fal[fid] = {};
        $('#id_personas :selected').each(function(i,s){
            add_permission(fid,ele,$(s).val(),$(s).text());
        });
    });
}

function update_persona_perm(persona){
        view.persona_perms[persona] = $('#'+persona+'_perm').val();
}

function view_updated(data){
    window.location = "/view/";
    return true;
}

function send_view(add,vid){
    if($('#id_name').val() == ""){ alert('View name cannot be blank'); return false; }
    if(add == true){
        $.ajax({url:'/view/add/',type:'post',data:{'fal':view.get_fal(),'name':$('#id_name').val(),'fields':$('#id_fields').val()},success:view_updated});
    }
    else{
        $.ajax({url:'/view/'+vid+'/',type:'post',data:{'fal':view.get_fal(),'name':$('#id_name').val(),'fields':$('#id_fields').val()},success:view_updated});
    }
}

function View(){

    this.perm_options = "<option value='rw'>Read-Write</option>"+
                        "<option value='r-'>Read-Only</option>" +
                        "<option value='-w'>Write-Only</option>" +
                        "<option value='rn'>Read-Restricted</option>" +
                        "<option value='nw'>Write-Restricted</option>";

    this.fal = {};

    this.persona_perms = {};

    this.init = function(){
    };

    this.get_fal = function(){
        return JSON.stringify(this.fal);
    };

    this.load_fal = function(){
        
    };

       
}
