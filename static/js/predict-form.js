mdc_list = ['#state-list', '#district-list', '#market-list', '#variety-list']

function getOptions(url, mdc_list_idx) {
    var request = new XMLHttpRequest();
    request.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            const states = JSON.parse(this.responseText)
            $(mdc_list[mdc_list_idx]).text('')
            for(var i = 0; i < states.length; i++) {
                $(mdc_list[mdc_list_idx]).append(`<li class="mdc-list-item" data-value="${i}">${states[i]}</li>`)
            }
        }
    };

    request.open("GET", url, true);
    request.send();
}

$(window).ready(getOptions('/api/states', 0))

mdcSelects[0].listen('MDCSelect:change', function() {
    if(mdcSelects[0].selectedIndex == -1)
        return

    $('#state-helper-text').css('opacity', '0')

    for(var i = 1; i < 4; i++) {
        $(mdcSelects[i]).text("")
        mdcSelects[i].selectedIndex = -1
    }

    getOptions(`/api/districts/${mdcSelects[0].selectedIndex}`, 1)
});

mdcSelects[1].listen('MDCSelect:change', function() {
    if(mdcSelects[1].selectedIndex == -1)
        return

    $('#district-helper-text').css('opacity', '0')

    for(var i = 2; i < 4; i++) {
        $(mdcSelects[i]).text("")
        mdcSelects[i].selectedIndex = -1
    }

    getOptions(`/api/markets/${mdcSelects[0].selectedIndex}/${mdcSelects[1].selectedIndex}`, 2)
});

mdcSelects[2].listen('MDCSelect:change', function() {
    if(mdcSelects[2].selectedIndex == -1)
        return

    $(mdcSelects[3]).text("")
    mdcSelects[3].selectedIndex = -1
    
    $('#market-helper-text').css('opacity', '0')
    getOptions(`/api/variety/${mdcSelects[0].selectedIndex}/${mdcSelects[1].selectedIndex}/${mdcSelects[2].selectedIndex}`, 3)
});

mdcSelects[3].listen('MDCSelect:change', function() {
    $('#variety-helper-text').css('opacity', '0')
});