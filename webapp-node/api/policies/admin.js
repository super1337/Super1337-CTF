module.exports=function(req,res,ok){

	if(req.session.User && req.session.User.admin){
		return ok();
	}

	else{
		var adminErr = ["You need to be admin."]
		req.session.flash={
			err:adminErr
		}
		res.redirect('/session/login');
		return;
	}

}