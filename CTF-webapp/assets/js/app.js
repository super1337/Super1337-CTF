(function (io){

	var socket=io.connect();
	if(typeof console!='undefined'){
		log('connecting to sials.js...');
	}

	socket.on('connect',function socketConnected(){

		console.log("This is from the connect: ",this.socket.sessionid);

		socket.on('message',function messageReceived(message){


			log('New comet message received :: ',message);

		});

		socket.get('user/subscribe');
	})

})