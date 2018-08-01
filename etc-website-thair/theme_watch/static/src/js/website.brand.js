$(document).ready(function() {
    $("#as_our_brand").owlCarousel({
        items: 6,
        margin: 10,
        navigation: true,
        pagination: false,
        responsive: {
            0: {
                items: 2,
            },
            481: {
                items: 2,
            },
            768: {
                items: 4,
            },
            1024: {
                items: 8,
            }
        }

    });
});
