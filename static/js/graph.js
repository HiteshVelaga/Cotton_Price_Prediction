var chart = new Chart($('#price-graph'), {
    type: 'line',
    data: {
        datasets: [{
            label: "Historical",
            backgroundColor: 'rgba(0, 0, 0, 0.3)',
            borderColor: 'rgba(0, 0, 0, 0.3)',
            fill: false
        },
        {
            label: "Predicted",
            backgroundColor: $(':root').css('--mdc-theme-secondary'),
            borderColor: $(':root').css('--mdc-theme-secondary'),
            fill: false
        }]
    },
    options: {
        hover: {
            mode: 'nearest'
        },
        scales: {
            xAxes: [{
                display: true,
                scaleLabel: {
                    display: true,
                    labelString: "Date"
                }
            }],
            yAxes: [{
                display: true,
                scaleLabel: {
                    display: true,
                    labelString: "Price (₹)"
                }
            }]
        }
    }
})

var first = true

$('#predict-form').submit(function(event) {
    tabbar.activateTab(0)
    event.preventDefault()
    getPredictions(0)
})

tabbar.listen('MDCTabBar:activated', (event) => {
    getPredictions(event.detail.index)
});

function getPredictions(mode) {
    const state = parseInt(mdcSelects[0].value)
    const dist = parseInt(mdcSelects[1].value)
    const market = parseInt(mdcSelects[2].value)
    const variety = parseInt(mdcSelects[3].value)

    if(isNaN(state)) {
        $('#state-helper-text').css('opacity', '1')
        return
    } else if(isNaN(dist)) {
        $('#district-helper-text').css('opacity', '1')
        return
    } else 
    if(isNaN(market)) {
        $('#market-helper-text').css('opacity', '1')
        return
    } else 
    if(isNaN(variety)) {
        $('#variety-helper-text').css('opacity', '1')
        return
    }

    $('.price-card').fadeIn(1000)
    $('.graph-card').fadeIn(1000)
    $('html, body').animate({
        scrollTop: $(".graph-card").offset().top
    }, 500);
    console.log(mode)
    getData(state, dist, market, variety, mode)
}

function getHistLen(mode) {
    switch(mode) {
        case 1:
        case 2:
            return 8
        default:
            return 14
    }
}

function getPredLen(mode) {
    switch(mode) {
        case 1:
            return 4
        case 2:
            return 8
        default:
            return 7
    }
}

function getDates(start, len, multiple) {
    var arr = new Array()

    while(len>0) {
        start.setDate(start.getDate() + 1 * multiple)
        arr.push(start.toLocaleDateString('en-GB', {
            day: 'numeric', month: '2-digit', year: 'numeric'
          }).replace(/\//g, '-'))
        len--;
    }

    return arr
}

function getDatesAfter(start, len) {
    return getDates(start, len, 1)
}

function getDatesBefore(start, len) {
    return getDates(start, len, -1)
}

function getData(state, dist, market, variety, mode) {
    var hData = new Array()
    var pData = new Array()

    var histReq = new XMLHttpRequest();
    var predReq = new XMLHttpRequest();

    histReq.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            hData = JSON.parse(this.responseText);
            display(mode, hData, pData)
        }
    };
    histReq.open("GET", `/api/history/${state}/${dist}/${market}/${variety}/${mode}/${getHistLen(mode)}`, true);


    predReq.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            pData = JSON.parse(this.responseText);
            histReq.send()
        }
    };
    predReq.open("GET", `/api/predict/${state}/${dist}/${market}/${variety}/${mode}/${getPredLen(mode)}`, true);

    predReq.send();
}

function display(mode, hData, pData) {
    const hDates = getDatesBefore(new Date(), hData.length)
    const pDates = getDatesAfter(new Date(), pData.length)
    
    const duration = (first)? 0 : 500
    first = false

    const price = $('#price-container')
    price.slideUp(duration, function() {
        price.text("")

        for(var i = 0; i < pDates.length; i++) {
            const price = pData[i].toLocaleString('en-IN', {
                maximumFractionDigits: 2,
                style: 'currency',
                currency: 'INR'
            })
    
            $('#price-container').append(
                `<div class="price-item"> \
                    <div class="price mdc-typography--headline5">${price}</div> \
                    <div class="date mdc-typography--body2">on ${pDates[i]}</div> \
                    </div>`
            )
        }

        price.slideDown(duration)

        setGraphTitle(mode)
        plotGraph(hDates, hData, pDates, pData)
    })
}

function setGraphTitle(mode) {
    const title = $('#graph-title')
    title.fadeOut("fast", function() {
        title.text("Predicted Cotton Prices for next ")
        switch(mode) {
            case 1:
                title.append("month ")
                break
            case 2:
                title.append("two months ")
                break
            default:
                title.append("week ")
                break
        }
        title.append("(in ₹)")
        title.fadeIn("fast")
    })
}

function plotGraph(hDates, hData, pDates, pData) {
    const labels = hDates.concat(pDates)
    
    pDates.unshift(hDates[hDates.length - 1])
    pData.unshift(hData[hData.length - 1])

    for(var i = 0; i < hData.length; i++)
        hData[i] = {x: hDates[i], y: hData[i]}

    for(var i = 0; i < pData.length; i++)
        pData[i] = {x: pDates[i], y: pData[i]}
    
    chart.data.labels = labels
    chart.data.datasets[0].data = hData
    chart.data.datasets[1].data = pData

    chart.update();
}

$("#graph-save").click(function() {
    const canvas = document.getElementById('price-graph')
    const context = canvas.getContext('2d')
    const backgroundColor = 'rgb(255, 255, 255)'
    const w = canvas.width;
	const h = canvas.height;
    
	var data;
 
	if(backgroundColor) {
		data = context.getImageData(0, 0, w, h);
		var compositeOperation = context.globalCompositeOperation;
		context.globalCompositeOperation = "destination-over";
		context.fillStyle = backgroundColor;
		context.fillRect(0,0,w,h);
    }
    
	var imageData = canvas.toDataURL("image/png");
 
	if(backgroundColor) {
		context.clearRect (0,0,w,h);
		context.putImageData(data, 0,0);
		context.globalCompositeOperation = compositeOperation;
    }
    
    saveAs(imageData, "graph.png")
})