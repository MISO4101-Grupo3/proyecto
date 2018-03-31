
function  init() {
    $(".sidebar input[type='checkbox']").prop('checked', true)

    // Inicializar filtros tipos de acuerdo al parametro t
    var tipos = getParameterByName('t');
    if (tipos != undefined) {
        if(!tipos.includes('a'))
        {
            $("#resua").prop('checked', false)
        }
        if(!tipos.includes('l'))
        {
            $("#resul").prop('checked', false)
        }
        if(!tipos.includes('h'))
        {
            $("#resuh").prop('checked', false)
        }
        if(!tipos.includes('u'))
        {
            $("#resuu").prop('checked', false)
        }
        tipos = tipos.split(',');
    }
    else{
        tipos = getDataValues('resultado');
    }

    // Inicializar filtros de disciplinas de acuerdo al parametro d
    var disciplinas = getParameterByName('d');
    if (disciplinas != undefined) {
        $(".sidebar .disciplina").prop('checked', false)
        disciplinas = disciplinas.split(',');
        disciplinas.forEach(function (id) {
            $("#disci"+id).prop('checked', true)
        })
    }
    else{
        disciplinas = getDataValues('disciplina');
    }

    // Inicializar filtros de estrategías de acuerdo al parametro e
    var estrategias = getParameterByName('e');
    if (estrategias != undefined) {
        $(".sidebar .estrategia").prop('checked', false)
        estrategias = estrategias.split(',');
        estrategias.forEach(function (id) {
            $("#estra"+id).prop('checked', true)
        })
    }
    else{
        estrategias = getDataValues('estrategia');
    }

    // Inicializar href de los enlaces de los filtros de resultados
    $(".resultado").each(function (index, ele) {
        setFiltersLink(tipos,'res','t',ele);
    });

    // Inicializar href de los enlaces de los filtros de disciplinas
    $(".disciplina").each(function (index, ele) {
        setFiltersLink(disciplinas,'disc','d',ele);
    })

    // Inicializar href de los enlaces de los filtros de estrategías
    $(".estrategia").each(function (index, ele) {
        setFiltersLink(estrategias,'estr','e',ele);
    })

}

var $grid;

function setFiltersLink(base_arr, anchor_class,query_param, ele){
    var arr = JSON.parse(JSON.stringify(base_arr));
    var value = $(ele).attr('data-value');
    var idx = arr.indexOf(value);
    if(idx !== -1){
        arr.splice(idx, 1);
    }
    else arr.push(value);
    var param = arr.join(",");
    var obj = {sc:0,p:1};
    obj[query_param] = param;
    var href = getHref('',obj)
    $("#" + anchor_class + value).attr('href', href);
}

function  getDataValues(class_name) {
    var res = []
    $("."+class_name).each(function (index, ele) {
        var value = $(ele).attr('data-value');
        res.push(value);
    })
    return res;
}

/**
 * Retorna el parametro de la url con el nombre dado si existe. El segundo parametro es opcional
 * en caso de no existir se tomara la url actual.
 */
function getParameterByName(name, url) {
    if (!url) url = window.location.href;
    name = name.replace(/[\[\]]/g, "\\$&");
    var regex = new RegExp("[?&]" + name + "(=([^&#]*)|&|#|$)"),
        results = regex.exec(url);
    if (!results) return null;
    if (!results[2]) return '';
    return decodeURIComponent(results[2].replace(/\+/g, " "));
}

function bajarSiHayResultados() {
    if (window.location.search != "" ) {

        if(getParameterByName('sc') === '0') {
            var top = $(".sct-color-2").offset().top + 50;
            $('html, body').scrollTop(top);
            //window.location.hash = 'resultados'
        }
        else{
            $('html, body').animate({
                scrollTop: $(".sct-color-2").offset().top + 50
            }, 1500);
        }

    }
}

function mostrarBusquedaBasica() {
    $('.basic-search-input').removeClass('col-lg-3');
    $('.basic-search-input').addClass('col-lg-9');

    $("select[name='d']").val("");
    $("select[name='e']").val("");
    $('.advanced-search-input').hide();

    $('.basic-search-button').hide();
    $('.advanced-search-button').show();
}

function mostrarBusquedaAvanzada() {
    $('.basic-search-input').removeClass('col-lg-9');
    $('.basic-search-input').addClass('col-lg-3');

    $('.advanced-search-input').show();

    $('.advanced-search-button').hide();
    $('.basic-search-button').show();
}

/**
 * Retorna un href para el host dado con los query params especificados
 * @param host
 * @param params Objeto con los parametros del query. ej: {q:'hola', p:2}
 * @returns {string}
 */
function getHref(host,params){
    var query_params = new URLSearchParams(location.search);
    for(var key in params){
        query_params.set(key,params[key]);
    }
    return host+"?"+query_params.toString();
}
