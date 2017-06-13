/**
 * User.js
 *
 * @description :: TODO: You might write a short summary of how this model works and what it represents here.
 * @docs        :: http://sailsjs.org/documentation/concepts/models-and-orm/models
 */

module.exports = {

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

  },
};
