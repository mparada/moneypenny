function activate_buttons(){
	$('.transaction-ok').click(
		function(){
			card = this.parentElement.parentElement;
			card.remove();
		});
};

function add_transaction(text) {
	container = $('#notification-container');
	container.append(`<div class="card" style="display: none;">
	  <div class="card-block">
		<h4 class="card-title">Transaction</h4>
		<p class="card-text">` + text + `.</p>
		<a href="javascript:void(null);" class="card-link transaction-ok">Ok</a>
		<a href="javascript:void(null);" class="card-link">View transaction</a>
	  </div>
	</div>`);
	$(".card").show('slow');
	activate_buttons();
};

function add_support(text) {
	container = $('#notification-container');
	container.append(`<div class="card" style="display: none;">
	  <div class="card-block">
		<h4 class="card-title">Customer Support</h4>
		<p class="card-text">` + text + `.</p>
		<a href="javascript:void(null);" class="card-link transaction-ok">Ok</a>
		<a href="javascript:void(null);" class="card-link">View profile</a>
	  </div>
	</div>`)
	$(".card").show('slow');
	activate_buttons();
};

function add_balance(text) {
	container = $('#notification-container');
	container.append(`<div class="card" style="display: none;">
	  <div class="card-block">
		<h4 class="card-title">Balance</h4>
		<p class="card-text">` + text + `.</p>
		<a href="javascript:void(null);" class="card-link transaction-ok">Ok</a>
	  </div>
	</div>`);
	$(".card").show('slow');
	activate_buttons();
};

$(document).ready(
 	function(){
		activate_buttons();
	}
);
