/**
 * AdminController
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

		Admin.create(req.params.all(),function adminCreated(err,user){
			if(err) return next(err);
			res.json(admin);
		});
	},

};
