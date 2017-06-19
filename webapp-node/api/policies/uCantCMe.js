module.exports=function(req,res,next){
	var idMatch = req.session.User.id===req.param('id');
	var isAdmin = req.session.User.admin;

	if(!(idMatch || isAdmin)){
		var rightErr = ['You need to be admin.']
		req.session.flash={
			err:rightErr
		}
		res.redirect('/session/login');
		return;
	}

	next();
}