（function（$）{

	'使用严格';

	if（typeof wpcf7 ==='undefined'|| wpcf7 === null）{
		返回;
	}

	wpcf7 = $ .extend（{
		缓存：0，
		输入：[]
	}，wpcf7）;

	$（function（）{
		wpcf7.supportHtml5 =（function（）{
			var features = {};
			var input = document.createElement（'input'）;

			输入中的features.placeholder ='placeholder';

			var inputTypes = ['email'，'url'，'tel'，'number'，'range'，'date'];

			$ .each（inputTypes，function（index，value）{
				input.setAttribute（'type'，value）;
				features [value] = input.type！=='text';
			}）;

			返回功能;
		}）（）;

		$（'div.wpcf7> form'）.each（function（）{
			var $ form = $（this）;

			$ form.submit（function（event）{
				if（typeof window.FormData！=='function'）{
					返回;
				}

				wpcf7.submit（$ form）;
				event.preventDefault（）;
			}）;

			$( '.wpcf7-submit', $form ).after( '<span class="ajax-loader"></span>' );

			wpcf7.toggleSubmit( $form );

			$form.on( 'click', '.wpcf7-acceptance', function() {
				wpcf7.toggleSubmit( $form );
			} );

			// Exclusive Checkbox
			$( '.wpcf7-exclusive-checkbox', $form ).on( 'click', 'input:checkbox', function() {
				var name = $( this ).attr( 'name' );
				$form.find( 'input:checkbox[name="' + name + '"]' ).not( this ).prop( 'checked', false );
			} );

			// Free Text Option for Checkboxes and Radio Buttons
			$( '.wpcf7-list-item.has-free-text', $form ).each( function() {
				var $ freetext = $（'：input.wpcf7-free-text'，this）;
				var $ wrap = $（this）.closest（'.wpcf7-form-control'）;

				if（$（'：checkbox，：radio'，this）.is（'：checked'））{
					$ freetext.prop（'disabled'，false）;
				} else {
					$ freetext.prop（'disabled'，true）;
				}

				$ wrap.on（'change'，'：checkbox，：radio'，function（）{
					var $ cb = $（'.has-free-text'，$ wrap）.find（'：checkbox，：radio'）;

					if（$ cb.is（'：checked'））{
						$ freetext.prop（'disabled'，false）.focus（）;
					} else {
						$ freetext.prop（'disabled'，true）;
					}
				}）;
			}）;

			//占位符后退
			if（！wpcf7.supportHtml5.placeholder）{
				$（'[placeholder]'，$ form）.each（function（）{
					$（this）.val（$（this）.attr（'placeholder'））;
					$（this）.addClass（'placeholder'）;

					$（this）.focus（function（）{
						if（$（this）.hasClass（'placeholder'））{
							$（this）.val（''）.removeClass（'placeheld'）;
						}
					}）;

					$（this）.blur（function（）{
						if（''=== $（this）.val（））{
							$（this）.val（$（this）.attr（'placeholder'））;
							$（this）.addClass（'placeheld'）;
						}
					}）;
				}）;
			}

			if（wpcf7.jqueryUi &&！wpcf7.supportHtml5.date）{
				$ form.find（'input.wpcf7-date [type =“date”]'）.each（function（）{
					$（this）.datepicker（{
						dateFormat：'yy-mm-dd'，
						minDate：new Date（$（this）.attr（'min'）），
						maxDate：new Date（$（this）.attr（'max'））
					}）;
				}）;
			}

			if（wpcf7.jqueryUi &&！wpcf7.supportHtml5.number）{
				$ form.find（'input.wpcf7-number [type =“number”]'）.each（function（）{
					$（this）.spinner（{
						min：$（this）.attr（'min'），
						最大：$（this）.attr（'max'），
						步骤：$（this）.attr（'step'）
					}）;
				}）;
			}

			//字符数
			$（'.wpcf7-character-count'，$ form）.each（function（）{
				var $ count = $（this）;
				var name = $ count.attr（'data-target-name'）;
				var down = $ count.hasClass（'down'）;
				var starting = parseInt（$ count.attr（'data-starting-value'），10）;
				var maximum = parseInt（$ count.attr（'data-maximum-value'），10）;
				var minimum = parseInt（$ count.attr（'data-minimum-value'），10）;

				var updateCount = function（target）{
					var $ target = $（target）;
					var length = $ target.val（）。length;
					var count = down？起始长度：长度;
					$ count.attr（'data-current-value'，count）;
					$ count.text（count）;

					如果（最大&&最大<长度）{
						$ count.addClass（'too-long'）;
					} else {
						$ count.removeClass（'too-long'）;
					}

					如果（最小&&长度<最小）{
						$ count.addClass（'too-short'）;
					} else {
						$ count.removeClass（'too-short'）;
					}
				};

				$（'：input [name =''+ name +'“]'，$ form）.each（function（）{
					updateCount（this）;

					$（this）.keyup（function（）{
						updateCount（this）;
					}）;
				}）;
			}）;

			$ form.on（'change'，'。wpcf7-validates-as-url'，function（）{
				var val = $ .trim（$（this）.val（））;

				//检查方案部分
				if（val &&！val.match（/^[az][a-z0-9.+-]*:/i））{
					val = val.replace（/ ^ \ / + /，''）;
					val ='http：//'+ val;
				}

				$（this）.val（val）;
			}）;

			if（wpcf7.cached）{
				wpcf7.refill（$ form）;
			}
		}）;
	}）;

	wpcf7.getId = function（form）{
		return parseInt（$（'input [name =“_ wpcf7”]'，form）.val（），10）;
	};

	wpcf7.submit = function（form）{
		var $ form = $（form）;

		$（'[placeholder] .placeheld'，$ form）.each（function（i，n）{
			$（n）.val（''）;
		}）;

		wpcf7.clearResponse（$ form）;
		$（'.ajax-loader'，$ form）.addClass（'is-active'）;

		if（typeof window.FormData！=='function'）{
			返回;
		}

		var formData = new FormData（$ form.get（0））;

		var ajaxSuccess = function（data，status，xhr，$ form）{
			var detail = {
				id：$（data.into）.attr（'id'），
				status：data.status，
				输入：[]
			};

			$ .each（$ form.serializeArray（），function（i，field）{
				if（'_wpcf7'== field.name）{
					detail.contactFormId = field.value;
				} else if（'_wpcf7_version'== field.name）{
					detail.pluginVersion = field.value;
				} else if（'_wpcf7_locale'== field.name）{
					detail.contactFormLocale = field.value;
				} else if（'_wpcf7_unit_tag'== field.name）{
					detail.unitTag = field.value;
				} else if（'_wpcf7_container_post'== field.name）{
					detail.containerPostId = field.value;
				} else if（field.name.match（/ ^ _ /））{
					// 没做什么
				} else {
					detail.inputs.push（field）;
				}
			}）;

			var $ message = $（'.wpcf7-response-output'，$ form）;

			开关（data.status）{
				案例'validation_failed'：
					$.each( data.invalidFields, function( i, n ) {
						$( n.into, $form ).each( function() {
							wpcf7.notValidTip( this, n.message );
							$( '.wpcf7-form-control', this ).addClass( 'wpcf7-not-valid' );
							$( '[aria-invalid]', this ).attr( 'aria-invalid', 'true' );
						} );
					} );

					$message.addClass( 'wpcf7-validation-errors' );
					$form.addClass( 'invalid' );

					wpcf7.triggerEvent( data.into, 'invalid', detail );
					break;
				case 'spam':
					$message.addClass( 'wpcf7-spam-blocked' );
					$form.addClass( 'spam' );

					$( '[name="g-recaptcha-response"]', $form ).each( function() {
						if ( '' === $( this ).val() ) {
							var $ recaptcha = $（this）.closest（'.wpcf7-form-control-wrap'）;
							wpcf7.notValidTip（$ recaptcha，wpcf7.recaptcha.messages.empty）;
						}
					}）;

					wpcf7.triggerEvent（data.into，'spam'，detail）;
					打破;
				大小写'mail_sent'：
					$ message.addClass（'wpcf7-mail-sent-ok'）;
					$ form.addClass（'sent'）;

					if（data.onSentOk）{
						$ .each（data.onSentOk，function（i，n）{eval（n）}）;
					}

					wpcf7.triggerEvent（data.into，'mailsent'，detail）;
					打破;
				案例'mail_failed'：
				案例'acceptance_missing'：
				默认：
					$ message.addClass（'wpcf7-mail-sent-ng'）;
					$ form.addClass（'failed'）;

					wpcf7.triggerEvent（data.into，'mailfailed'，detail）;
			}

			wpcf7.refill（$ form，data）;

			if（data.onSubmit）{
				$.each( data.onSubmit, function( i, n ) { eval( n ) } );
			}

			wpcf7.triggerEvent（data.into，'submit'，detail）;

			if（'mail_sent'== data.status）{
				$ form.each（function（）{
					this.reset（）;
				}）;
			}

			$ form.find（'[placeholder] .placeheld'）.each（function（i，n）{
				$（n）.val（$（n）.attr（'placeholder'））;
			}）;

			$ message.append（data.message）.slideDown（'fast'）;
			$ message.attr（'role'，'alert'）;

			$（'。screen-reader-response'，$ form.closest（'。wpcf7'））。each（function（）{
				var $ response = $（this）;
				$ response.html（''）.attr（'role'，''）.append（data.message）;

				if（data.invalidFields）{
					var $ invalids = $（'<ul> </ ul>'）;

					$ .each（data.invalidFields，function（i，n）{
						if（n.idref）{
							var $li = $( '<li></li>' ).append( $( '<a></a>' ).attr( 'href', '#' + n.idref ).append( n.message ) );
						} else {
							var $li = $( '<li></li>' ).append( n.message );
						}

						$invalids.append( $li );
					} );

					$response.append( $invalids );
				}

				$response.attr( 'role', 'alert' ).focus();
			} );
		};

		$.ajax( {
			type: 'POST',
			url: wpcf7.apiSettings.root + wpcf7.apiSettings.namespace +
				'/contact-forms/' + wpcf7.getId( $form ) + '/feedback',
			data: formData,
			dataType: 'json',
			processData: false,
			contentType: false
		} ).done( function( data, status, xhr ) {
			ajaxSuccess( data, status, xhr, $form );
			$（'。ajax-loader'，$ form）.removeClass（'is-active'）;
		} .fail（function（xhr，status，error）{
			var $ e = $（'<div class =“ajax-error”> </ div>'）.text（error.message）;
			$ form.after（$ e）;
		}）;
	};

	wpcf7.triggerEvent = function（target，name，detail）{
		var $ target = $（target）;

		/ * DOM事件* /
		var event = new CustomEvent（'wpcf7'+ name，{
			泡泡：真的，
			细节：细节
		}）;

		$ target.get（0）.dispatchEvent（event）;

		/ * jQuery事件* /
		$ target.trigger（'wpcf7：'+ name，detail）;
		$ target.trigger（name +'.wpcf7'，detail）; / /弃用
	};

	wpcf7.toggleSubmit = function（form，state）{
		var $ form = $（form）;
		var $ submit = $（'input：submit'，$ form）;

		if（typeof state！=='undefined'）{
			$ submit.prop（'disabled'，！state）;
			返回;
		}

		if（$ form.hasClass（'wpcf7-acceptance-as-validation'））{
			返回;
		}

		$ submit.prop（'disabled'，false）;

		$（'input：checkbox.wpcf7-acceptance'，$ form）.each（function（）{
			var $ a = $（this）;

			if（$ a.hasClass（'wpcf7-invert'）&& $ a.is（'：checked'））
			|| ！$ a.hasClass（'wpcf7-invert'）&&！$ a.is（'：checked'））{
				$ submit.prop（'disabled'，true）;
				返回false;
			}
		}）;
	};

	wpcf7.notValidTip =函数（目标，消息）{
		var $ target = $（target）;
		$（'.wpcf7-not-valid-tip'，$ target）.remove（）;
		$（'<span role =“alert”class =“wpcf7-not-valid-tip”> </ span>'）
			.text（message）.appendTo（$ target）;

		if（$ target.is（'.use-floating-validation-tip *'））{
			var fadeOut = function( target ) {
				$( target ).not( ':hidden' ).animate( {
					opacity: 0
				}, 'fast', function() {
					$( this ).css( { 'z-index': -100 } );
				} );
			}

			$target.on( 'mouseover', '.wpcf7-not-valid-tip', function() {
				fadeOut( this );
			} );

			$target.on( 'focus', ':input', function() {
				fadeOut( $( '.wpcf7-not-valid-tip', $target ) );
			} );
		}
	}

	wpcf7.refill = function( form, data ) {
		var $form = $( form );

		var refillCaptcha = function( $form, items ) {
			$.each( items, function( i, n ) {
				$form.find( ':input[name="' + i + '"]' ).val( '' );
				$form.find( 'img.wpcf7-captcha-' + i ).attr( 'src', n );
				var match = /([0-9]+)\.(png|gif|jpeg)$/.exec( n );
				$form.find( 'input:hidden[name="_wpcf7_captcha_challenge_' + i + '"]' ).attr( 'value', match[ 1 ] );
			} );
		};

		var refillQuiz = function( $form, items ) {
			$.each( items, function( i, n ) {
				$form.find( ':input[name="' + i + '"]' ).val( '' );
				$form.find( ':input[name="' + i + '"]' ).siblings( 'span.wpcf7-quiz-label' ).text( n[ 0 ] );
				$form.find( 'input:hidden[name="_wpcf7_quiz_answer_' + i + '"]' ).attr( 'value', n[ 1 ] );
			} );
		};

		if ( typeof data === 'undefined' ) {
			$.ajax( {
				type: 'GET',
				url: wpcf7.apiSettings.root + wpcf7.apiSettings.namespace +
					'/contact-forms/' + wpcf7.getId( $form ) + '/refill',
				dataType: 'json'
			} ).done( function( data, status, xhr ) {
				if ( data.captcha ) {
					refillCaptcha( $form, data.captcha );
				}

				if ( data.quiz ) {
					refillQuiz( $form, data.quiz );
				}
			} );

		} else {
			if ( data.captcha ) {
				refillCaptcha( $form, data.captcha );
			}

			if ( data.quiz ) {
				refillQuiz( $form, data.quiz );
			}
		}
	};

	wpcf7.clearResponse = function( form ) {
		var $form = $( form );
		$form.removeClass( 'invalid spam sent failed' );
		$form.siblings( '.screen-reader-response' ).html( '' ).attr( 'role', '' );

		$( '.wpcf7-not-valid-tip', $form ).remove();
		$( '[aria-invalid]', $form ).attr( 'aria-invalid', 'false' );
		$( '.wpcf7-form-control', $form ).removeClass( 'wpcf7-not-valid' );

		$( '.wpcf7-response-output', $form )
			.hide().empty().removeAttr( 'role' )
			.removeClass( 'wpcf7-mail-sent-ok wpcf7-mail-sent-ng wpcf7-validation-errors wpcf7-spam-blocked' );
	};

} )( jQuery );

/*
 * Polyfill for Internet Explorer
 * See https://developer.mozilla.org/en-US/docs/Web/API/CustomEvent/CustomEvent
 */
( function () {
	if ( typeof window.CustomEvent === "function" ) return false;

	function CustomEvent ( event, params ) {
		params = params || { bubbles: false, cancelable: false, detail: undefined };
		var evt = document.createEvent( 'CustomEvent' );
		evt.initCustomEvent( event,
			params.bubbles, params.cancelable, params.detail );
		return evt;
	}

	CustomEvent.prototype = window.Event.prototype;

	window.CustomEvent = CustomEvent;
} )();