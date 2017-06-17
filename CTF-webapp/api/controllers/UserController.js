/**
 * UserController
 *
 * @description :: Server-side logic for managing users
 * @help        :: See http://sailsjs.org/#!/documentation/concepts/Controllers
 */

module.exports = {

	'signup':function(req,res){
		res.view();
	},
	'login':function(req,res){
		res.view();
	},

	create:function(req,res,next){

		User.create(req.params.all(),function userCreated(err,user){
			if(err) {
				console.log(err);
				req.session.flash={
					err:err
				}


				return res.redirect('/user/signup');
			}
			req.session.authenticated=true;
			req.session.User=user;
			user.online=true;
			//res.json(user);
			//req.session.flash={};
			user.save(function(err,User){
				if(err) return next(err);
			res.redirect('/user/postsign/'+user.id);
		});
		});
	},

	show:function(req,res,next){

		User.findOne(req.param('id'),function foundUser(err,user){

			if(err) return next(err);
			if(!user) return next();
			res.view({
				user:user
			});
		});
	},

	postsign:function(req,res,next){

		User.findOne(req.param('id'),function foundUser(err,user){

			if(err) return next(err);
			if(!user) return next();
			res.view({
				user:user
			});
		});
	},

	index:function(req,res,next){

		// console.log(new Date());
		// console.log(req.session.authenticated);

		User.find(function foundUser(err,users){

			if(err) return next(err);
			res.view({
				users:users
			});
		});
	},

	edit:function(req,res,next){

		User.findOne(req.param('id'),function foundUser(err,user){

			if(err) return next(err);
			if(!user) return next('User does\'t exists.');
			res.view({
				user:user
			});
		});
	},

	update:function(req,res,next){
		User.update(req.param('id'),req.params.all(),function userUpdated(err){
			if (err){
				return res.redirect('/user/edit/'+req.param('id'));
			}

			res.redirect('/user/postsign/'+req.param('id'));
		});
	},

	destroy:function(req,res,next){

		User.findOne(req.param('id'),function foundUser(err,user){

			if(err) return next(err);
			if(!user) return next('User does\'t exists.');

			User.destroy(req.param('id'),function userDestroyed(err){
				if (err) return next(err);
			});

			res.redirect('/user');

		});
	},

	subscribe:function(req,res){

		User.find(function foundUser(err,users){

			if(err) return next(err);

			User.subscribe(req.socket);

			User.subscribe(req.socket,users);
		})
	}



}
