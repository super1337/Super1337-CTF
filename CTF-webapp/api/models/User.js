/**
 * User.js
 *
 * @description :: TODO: You might write a short summary of how this model works and what it represents here.
 * @docs        :: http://sailsjs.org/documentation/concepts/models-and-orm/models
 */

module.exports = {

  schema:true,

  attributes: {
    name : {
      type:'string',
      required:true,
    },
    username:{
      type:'string',
      unique:true,
      required:true,
    },
    email:{
      type:'string',
      email:true,
      required:true,
      unique:true,
    },
    password:{
      type:'string',
      required:true,
    },
    sex:{
      type:'string',

    },
    level:{
      type:'string',

    },
    admin:{
      type:'boolean',
      defaultsTo:false,
    },

    toJSON:function(){
      var obj=this.toObject();
      delete obj.password;
      delete obj.passconf;
      delete obj._csrf;
      return obj;
    },

  },

  // beforeValidation : function(values,next){
  //   if(typeof values.admin !== 'undefined'){
  //     if(value.admin === 'unchecked'){
  //       values.admin=false;
  //     }
  //     else if(values.admin[1]==='on'){
  //       values.admin=true;
  //     }
  //   }
  //   next();
  // }


  beforeCreate : function(values,next){

    if(!values.password || values.password!=values.passconf){
      return next({err:["Password doesn't match."]});
    }

    require('bcrypt').hash(values.password,10,function passwordEncrypted(err,encryptedPassword){
      if (err) return next(err);
      values.password=encryptedPassword;
      // values.online=true;
      next();
    });
  }
};
