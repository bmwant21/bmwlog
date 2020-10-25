$(function() {

	var TransitionEffects	= (function() {

		var $teWrapper		= $('#te-wrapper'),
			$teCover		= $teWrapper.find('div.te-cover'),
			$teImages		= $teWrapper.find('div.te-images > img'),
			imagesCount		= $teImages.length,
			currentImg		= 0,
			type			= 'te-cube4',
			$teTransition	= $teWrapper.find('.te-transition'),
			// requires perspective
			wPerspective	= [ 'te-flip1', 'te-flip2', 'te-flip3', 'te-flip4',
								'te-rotation1', 'te-rotation2', 'te-rotation3', 'te-rotation4', 'te-rotation5',
								'te-multiflip1', 'te-multiflip2', 'te-multiflip3',
								'te-cube1', 'te-cube2', 'te-cube3', 'te-cube4',
								'te-unfold1', 'te-unfold2'],
			animated		= false,
			// check for support
			hasPerspective	= Modernizr.csstransforms3d,
			init			= function() {

				$teTransition.addClass( type );
				$teWrapper.on( 'mouseover', function( event ) {

					if( hasPerspective && animated )
						return false;

					animated = true;
					showNext();
					return false;

				});

                $teWrapper.on('mouseleave', function(event) {
                    showNext();
                    animated = false;
                });

				if( hasPerspective ) {

					$teWrapper.on({
						'webkitAnimationStart' : function( event ) {

						},
						'webkitAnimationEnd'   : function( event ) {

							if( ( type === 'te-unfold1' && event.originalEvent.animationName !== 'unfold1_3Back' ) ||
								( type === 'te-unfold2' && event.originalEvent.animationName !== 'unfold2_3Back' ) )
								return false;

							$teCover.removeClass('te-hide');
							if( $.inArray( type, wPerspective ) !== -1 )
								$teWrapper.removeClass('te-perspective');
							$teTransition.removeClass('te-show');
							//animated = false;

						}
					});

				}
			},
			showNext		= function() {

				if( hasPerspective ) {

					if( $.inArray( type, wPerspective ) !== -1 ) {

						$teWrapper.addClass('te-perspective');

					}
					$teTransition.addClass('te-show');
					$teCover.addClass('te-hide');


				}

				updateImages();

			},
			updateImages	= function() {

				var $back 	= $teTransition.find('div.te-back'),
					$front	= $teTransition.find('div.te-front');

				( currentImg === imagesCount - 1 ) ?
					( last_img = imagesCount - 1, currentImg = 0 ) :
					( last_img = currentImg, ++currentImg );

				var $last_img 	= $teImages.eq( last_img ),
					$currentImg	= $teImages.eq( currentImg );

				$front.empty().append('<img src="' + $last_img.attr('src') + '">');
				$back.empty().append('<img src="' + $currentImg.attr('src') + '">');

				$teCover.find('img').attr( 'src', $currentImg.attr('src') );

			};

		return { init : init };

	})();

	TransitionEffects.init();

});
