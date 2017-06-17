(function (io){

	var socket=io.connect();
	if(typeof console!='undefined'){
		log('connecting to sials.js...');
	}

	socket.on('connect',function socketConnected(){

		console.log("This is from the connect: ",socket.sessionid);

		socket.on('message',cometMsg);

		socket.get('user/subscribe');

		log('global connections OK');

});

window.socket=socket;

function log(){
	if (typeof console !=='undefined'){
		console.log.apply(console,arguments);
	}
}

})(

	window.io

);

function cometMsg(message){
	console.log("Here's the message: ",message);

	if(message.model==='user'){
		var userId=message.id
		updateUserInDom(userId,message);
	}
}

function updateUserInDom(userId,message){

	var page = document.location.pathname;

	page=page.replace(/(\/)$/,'');

	switch(page){

		case '/user':

		if (message.verb==='update'){
			UserIndexPage.updateUser(userId,message);
		}
		if (message.verb==='create'){
			UserIndexPage.addUser(message);
		}
		if (message.verb==='destroy'){
			UserIndexPage.destroyUser(message);
		}
		break;
	}
}

var UserIndexPage={

	updateUser:function(id,message){
		if (message.data.loggedIn){
			var $userRow = $('tr[data-id="'+id+'"] td img').first();
			$userRow.attr('src',"https://d19rpgkrjeba2z.cloudfront.net/dc25e9dfd0ebe580/static/nextdoorv2/images/icons/icon-check-ok@2x.png");
		} else {
			var $userRow = $('tr[data-id="'+id+'"] td img').first();
			$userRow.attr('src',"http://www.freeiconspng.com/uploads/remove-icon-png-15.png");
		}
	},
	addUser:function(user){
		var odj={
			user:user.data,
			_csrf:window.overload.csrf || ''
		}
		$('tr:last').after(
			JST[assets/templates/addUser.ejs](obj)
			);
	},
	destroyUser:function(id){
		$('tr[data-id="'+id+'"]').remove();
	}
}