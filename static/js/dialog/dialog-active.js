(function ($) {
 "use strict";
 
	/*----------------------
		Dialogs
	 -----------------------*/

	//Basic
	$('#sa-basic').on('click', function(){
		swal("Here's a message!");
	});

	//A title with a text under
	$('#sa-title').on('click', function(){
		swal("You can go!", "The cases have dropped drastically near you and it is safe to go!", "success")
		});

	//Success Message
	$('#sa-success1').on('click', function(){
		swal("You can go!", "The cases have dropped drastically near you and it is safe to go!", "success")
	});

	$('#sa-success2').on('click', function(){
		swal("You can go!", "The cases have dropped drastically near you and it is safe to go!", "success")
	});

	$('#sa-success3').on('click', function(){
		swal("You can go!", "The cases have dropped drastically near you and it is safe to go!", "success")
	});

	$('#sa-success4').on('click', function(){
		swal("You can go!", "The cases have dropped drastically near you and it is safe to go!", "success")
	});
	//Warning Message
	$('#sa-warning1').on('click', function(){
		swal({   
			title: "Are you sure?",   
			text: "Given the recent rise in cases, it might not be the safest course of action.",   
			type: "warning",   
			showCancelButton: true,   
			confirmButtonText: "Yes, I need to go!",
		})
	});

	$('#sa-warning2').on('click', function(){
		swal({   
			title: "Are you sure?",   
			text: "Given the recent rise in cases, it might not be the safest course of action.",   
			type: "warning",   
			showCancelButton: true,   
			confirmButtonText: "Yes, I need to go!",
		})
	});

	$('#sa-warning3').on('click', function(){
		swal({   
			title: "Are you sure?",   
			text: "Given the recent rise in cases, it might not be the safest course of action.",   
			type: "warning",   
			showCancelButton: true,   
			confirmButtonText: "Yes, I need to go!",
		})
	});
	
	
	$('#sa-warning4').on('click', function(){
		swal({   
			title: "Are you sure?",   
			text: "Given the recent rise in cases, it might not be the safest course of action.",   
			type: "warning",   
			showCancelButton: true,   
			confirmButtonText: "Yes, I need to go!",
		})
	});
	//Parameter
	$('#sa-params').on('click', function(){
		swal({   
			title: "Are you sure?",   
			text: "You will not be able to recover this imaginary file!",   
			type: "warning",   
			showCancelButton: true,   
			confirmButtonText: "Yes, delete it!",
			cancelButtonText: "No, cancel plx!",   
		}).then(function(isConfirm){
			if (isConfirm) {     
				swal("Deleted!", "Your imaginary file has been deleted.", "success");   
			} else {     
				swal("Cancelled", "Your imaginary file is safe :)", "error");   
			} 
		});
	});

	//Custom Image
	$('#sa-image').on('click', function(){
		swal({   
			title: "Sweet!",   
			text: "Here's a custom image.",   
			imageUrl: "img/dialog/like.png" 
		});
	});

	//Auto Close Timer
	$('#sa-close').on('click', function(){
		 swal({   
			title: "Auto close alert!",   
			text: "I will close in 2 seconds.",   
			timer: 2000
		});
	});

 
})(jQuery); 