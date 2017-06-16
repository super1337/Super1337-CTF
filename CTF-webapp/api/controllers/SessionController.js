/**
 * SessionController
 *
 * @description :: Server-side logic for managing sessions
 * @help        :: See http://sailsjs.org/#!/documentation/concepts/Controllers
 */

 var bcrypt=require('bcrypt');

module.exports = {

	'login':function(req,res){

		// var oldDateObj = new Date();
		// var newDateObj = new Date(oldDateObj.getTime()+60000);
		// req.session.cookie.expires=newDateObj;
		// req.session.authenticated=true;
		// console.log(req.session);
		res.view('user/login');
	},

	create:function(req,res,next){

		if(!req.param('username') || !req.param('password')){
			// var notfillerr = [{name:'notfillerr',message:'Enter both username and password.'}]
			var notfillerr = ['Enter both username and password.']

			req.session.flash={
				err:notfillerr
			}

			res.redirect('/session/login');
			return;
		}

		User.findOneByUsername(req.param('username'), function foundUser(err,user){
			if (err) return next(err);

			if(!user){
				// var notfounderr=[{name:'notfounderr',message:'Invalid Email-ID or Password'}]
				var notfillerr = ['Invalid Email-ID or Password']

				req.session.flash={
					err:notfounderr
				}

				res.redirect('/session/login');
				return;
			}

			bcrypt.compare(req.param('password'),user.password,function(err,valid){
				if (err) return next(err);

				if(!valid){
				// var notfounderr=[{name:'notfounderr',message:'Invalid Email-ID or Password'}]
				var notfillerr = ['Invalid Email-ID or Password']

				req.session.flash={
					err:notfounderr
				}

				res.redirect('/session/login');
				return;

				}

				req.session.authenticated=true;
				req.session.User=user;
				user.online=true;
			//res.json(user);
			//req.session.flash={};
			user.save(function(err){
				if(err) return next(err);

				if(req.session.User.admin){
					res.redirect('/user');
					return;
				}

				res.redirect('/user/show/'+user.id);
			});
			});

		});
	},

	destroy:function(req,res,next){

		User.findOne(req.session.User.id,function foundUser(err,user){
			var userID = req.session.User.id;

			User.update(userID,{
				online:false
			},function(err){
				if(err) return next(err);

				req.session.destroy();

				res.redirect('/session/login');
			})
		})

		
	}
	
};

