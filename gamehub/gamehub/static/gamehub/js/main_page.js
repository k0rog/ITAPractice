const ratingSlider = document.getElementById('target');

    noUiSlider.create(ratingSlider, {
        start: [5.0, 10.0],
        connect: true,
        margin: null,
        limit: null,
        step: 0.01,
        orientation: 'horizontal',
        tooltips: true,
        padding: 0,
        range: {
            'min': 0,
            'max': 10
        },
        pips: {
            mode: 'values',
            values: [5, 10],
            density: 5
        }
    });