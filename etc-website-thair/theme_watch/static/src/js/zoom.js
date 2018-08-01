$(document).ready(function() {

    $(".sub-images").click(function(ev) {
        ev.preventDefault();
      	ev.stopPropagation();
        $('.product_detail_img').attr('src', this.src);
        $('.product_detail_img').parent().parent().attr('src', this.src);
        $('.zoomContainer').remove();
        $('.product_detail_img').removeData('elevateZoom');
		$('.product_detail_img').elevateZoom({
                        constrainType: "height",
                        constrainSize: 274,
                        zoomType: "lens",
                        containLensZoom: true,
                        cursor: 'pointer'
                    });		

    });

    $(".zoom_02").hover(function() {
        s = this.src;
        $('.main_image').attr('src', this.src);
		$('.main_image').parent().attr('href',this.src);
        $('.zoomContainer').remove();
        $('.product_detail_img').removeData('elevateZoom');
		$('.product_detail_img').elevateZoom({
                        constrainType: "height",
                        constrainSize: 274,
                        zoomType: "lens",
                        containLensZoom: true,
                        cursor: 'pointer'
                    });

    });
    
});

