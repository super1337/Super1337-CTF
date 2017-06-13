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

    toJSON:function(){
      var obj=this.toObject();
      delete obj.password;
      delete obj.passconf;
      delete obj._csrf;
      return obj;
    }

  },
};
