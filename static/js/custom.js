$(document).ready( function() {
	var color_blue = '#4c8ffc';
       	var color_red = '#FF0000';
	var emptyImage = 'data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///ywAAAAAAQABAAACAUwAOw==';
	$(".alert-success").hide();
	$(".alert-danger").hide();
    	$(document).on('change', '.btn-file :file', function() {
		
		var input = $(this),
			label = input.val().replace(/\\/g, '/').replace(/.*\//, '');
		input.trigger('fileselect', [label]);
		});

		$('.btn-file :file').on('fileselect', function(event, label) {

		    var input = $(this).parents('.input-group').find(':text'),
		        log = label;


		    if( input.length ) {
		        input.val(log);
		    } else {
		        if( log ) alert(log);
		    }

		});
		function readURL(input, id) {
		    if (input.files && input.files[0]) {
		        var reader = new FileReader();

		        reader.onload = function (e) {
		            $(id).attr('src', e.target.result);
		        }

		        reader.readAsDataURL(input.files[0]);
		      
		    }
		}

		$("#imgInp").change(function(){
		    readURL(this, "#img-upload");

		});

		$("#misclassified-img").change(function(){
			readURL(this, "#misclassified-img-upload"); 
		});


		//send image to backend by pressing upload..

		$("#upload").on("click", function(){

		    //disable button after its been clicked
		    $("#upload").prop("disabled", true);

            //grab form data..
		    var form_data = new FormData($('#upload_image')[0]);

			ajaxCall("/predict_image", "#img-upload", form_data, "#upload");
		
		});

		// send misclassified image to backend..

		$("#upload-misclassified").on("click",function(){

			if ($("#misclassified-img-upload")[0].src === ""|| $("#misclassified-img-upload")[0].src === emptyImage){
				 $(".alert-danger").show(2000).hide(1000);	
			}
	
			else{
			//disbale button ..
			$("#upload-misclassified").prop("disabled", true);
			var form_data = new FormData($('#misclassified_image')[0]);
			ajaxCall("/misclassified_image", "#misclassified-img-upload", form_data, "#upload-misclassified",plot_chart=false)
			//alert("test");
			}

		});

    function ajaxCall(url,image_id,form_data, btn_id, plot_chart=true) {
		//send to backend...
            $.ajax
            ({
                    type: 'POST',
                    url: url,
                    data: form_data,
                    contentType: false,
                    cache: false,
                    processData: false,
                    success: function(data) {

                        //empty div contents to begin with before plotting new results.
                        $('#graph_01').empty();
                        $(image_id)[0].src = 'data:image/png;base64, ' + data.encoded_img;
						if (plot_chart){	
                        	plotBarchart(data.hotspot_prob, data.nohotspot_prob)
						}
                        //enable button 
                        $(btn_id).prop("disabled", false);
						//check if misclassified button pressed
						if ($(btn_id).attr("id") === "upload-misclassified"){

								$(".alert-success").show(2000).hide(1000);

								$('#misclassified-img-upload').attr('src',emptyImage); 
								$("#mis_img").val("");
						}

                    },
             });



	}
	function plotBarchart(hotspot_value, no_hotspot_value){
	 	$('#graph_01').dvstr_graph({
			title: 'Hotstpot detection analysis',
			grid_wmax:0,
			grid_part: 5,
			graphs:
			[
				{
					label:'Hotspot %',
					color:[color_red],
					value:[parseFloat((hotspot_value*100).toFixed(2))] 
				},
				{
					label: "No hotspot %", 
					color:[color_blue],
					value:[parseFloat((no_hotspot_value*100).toFixed(2))]

				},
			]
  
		});

	}

	});
